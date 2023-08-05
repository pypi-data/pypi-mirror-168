/*
 * super-call.m -- Finding the right dispatch function for a method-call
 *
 * This file defines a registry that is used to find the right function to
 * call when a method is called. There are 3 variants:
 *
 * - Call the method from python
 * - Call the python implementation of a method from Objective-C
 *
 * XXX: Add API to dump the registry for inspection.
 */
#include "pyobjc.h"

NS_ASSUME_NONNULL_BEGIN

/* XXX: Consider using a minimal python type instead of a capsule */
struct registry {
    PyObjC_CallFunc       call_to_objc;
    PyObjCFFI_ClosureFunc call_to_python;
};

/* Dict mapping from signature-string to a 'struct registry' */
static PyObject* signature_registry = (PyObject* _Nonnull)NULL;

/* Dict mapping from selector to a list of (Class, struct registry) tuples */
static PyObject* special_registry = (PyObject* _Nonnull)NULL;

/*
 * Initialize the data structures
 */
int
PyObjC_InitSuperCallRegistry(void)
{
    if (signature_registry == NULL) {
        signature_registry = PyDict_New();
        if (signature_registry == NULL) // LCOV_BR_EXCL_LINE
            return -1;                  // LCOV_EXCL_LINE
    }

    if (special_registry == NULL) {
        special_registry = PyDict_New();
        if (special_registry == NULL) // LCOV_BR_EXCL_LINE
            return -1;                // LCOV_EXCL_LINE
    }

    return 0;
}

static void
memblock_capsule_cleanup(PyObject* ptr)
{
    void* mem = PyCapsule_GetPointer(ptr, "objc.__memblock__");

#ifdef PyObjC_DEBUG
    if (mem == NULL)
        PyObjCErr_InternalError();
#endif

    PyMem_Free(mem);
}

/*
 * Add a custom mapping for a method in a class
 */
int
PyObjC_RegisterMethodMapping(_Nullable Class class, SEL sel, PyObjC_CallFunc call_to_objc,
                             PyObjCFFI_ClosureFunc call_to_python)
{
    struct registry* v;
    PyObject*        pyclass;
    PyObject*        entry;
    PyObject*        lst;

    if (!call_to_python) {
        PyErr_SetString(PyObjCExc_Error,
                        "PyObjC_RegisterMethodMapping: all functions required");
        return -1;
    }

    if (!call_to_objc) {
        call_to_objc = PyObjCFFI_Caller;
    }

    if (class == nil) {
        pyclass = Py_None;
        Py_INCREF(Py_None);
    } else {
        pyclass = PyObjCClass_New(class);
        if (pyclass == NULL) { // LCOV_BR_EXCL_LINE
            return -1;         // LCOV_EXCL_LINE
        }
    }

    v = PyMem_Malloc(sizeof(*v));
    if (v == NULL) { // LCOV_BR_EXCL_LINE
        // LCOV_EXCL_START
        PyErr_NoMemory();
        return -1;
        // LCOV_EXCL_STOP
    }
    v->call_to_objc   = call_to_objc;
    v->call_to_python = call_to_python;

    entry = PyTuple_New(2);
    if (entry == NULL) { // LCOV_BR_EXCL_LINE
        // LCOV_EXCL_START
        PyMem_Free(v);
        return -1;
        // LCOV_EXCL_STOP
    }

    PyTuple_SET_ITEM(entry, 0, pyclass);
    PyTuple_SET_ITEM(entry, 1,
                     PyCapsule_New(v, "objc.__memblock__", memblock_capsule_cleanup));

    if (PyTuple_GET_ITEM(entry, 1) == NULL) { // LCOV_BR_EXCL_LINE
        // LCOV_EXCL_START
        Py_DECREF(entry);
        return -1;
        // LCOV_EXCL_STOP
    }

    lst = PyDict_GetItemStringWithError(special_registry, sel_getName(sel));
    if (lst == NULL && PyErr_Occurred()) { // LCOV_BR_EXCL_LINE
        // LCOV_EXCL_START
        Py_DECREF(entry);
        return -1;
        // LCOV_EXCL_STOP
    } else if (lst == NULL) {
        lst = PyList_New(0);
        if (PyDict_SetItemString( // LCOV_BR_EXCL_LINE
                special_registry, sel_getName(sel), lst)
            == -1) {
            // LCOV_EXCL_START
            Py_DECREF(lst);
            Py_DECREF(entry);
            return -1;
            // LCOV_EXCL_STOP
        }
    } else {
        Py_INCREF(lst);
    }

    if (PyList_Append(lst, entry) < 0) { // LCOV_BR_EXCL_LINE
        // LCOV_EXCL_START
        Py_DECREF(lst);
        Py_DECREF(entry);
        return -1;
        // LCOV_EXCL_STOP
    }
    Py_DECREF(lst);
    Py_DECREF(entry);

    PyObjC_MappingCount += 1;

    return 0;
}

#if 0
int
PyObjC_RegisterSignatureMapping(char* signature, PyObjC_CallFunc call_to_objc,
                                PyObjCFFI_ClosureFunc call_to_python)
{
    struct registry* v;
    PyObject*        entry;
    char             signature_buf[1024];
    int              r;

    r = PyObjCRT_SimplifySignature(signature, signature_buf, sizeof(signature_buf));
    if (r == -1) {
        PyErr_SetString(PyObjCExc_Error, "cannot simplify signature");
        return -1;
    }

    if (!call_to_objc || !call_to_python) {
        PyErr_SetString(PyObjCExc_Error,
                        "PyObjC_RegisterSignatureMapping: all functions required");
        return -1;
    }

    v = PyMem_Malloc(sizeof(*v));
    if (v == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    v->call_to_objc   = call_to_objc;
    v->call_to_python = call_to_python;

    entry = PyCapsule_New(v, "objc.__memblock__", memblock_capsule_cleanup);
    if (entry == NULL) {
        PyMem_Free(v);
        return -1;
    }

    PyObject* key = PyBytes_FromString(signature_buf);
    if (key == NULL) {
        return -1;
    }

    if (PyDict_SetItem(signature_registry, key, entry) < 0) {
        Py_DECREF(key);
        Py_DECREF(entry);
        return -1;
    }
    Py_DECREF(key);
    Py_DECREF(entry);
    PyObjC_MappingCount += 1;

    return 0;
}
#endif

/*
 * May of may not raise an exception when the return value is NULL
 */
static struct registry* _Nullable search_special(Class class, SEL sel)
{
    PyObject*  result        = NULL;
    PyObject*  special_class = NULL;
    PyObject*  search_class  = NULL;
    PyObject*  lst;
    Py_ssize_t i;

    if (special_registry == NULL)
        goto error;
    if (!class)
        goto error;

    search_class = PyObjCClass_New(class);
    if (search_class == NULL) // LCOV_BR_EXCL_LINE
        goto error;           // LCOV_EXCL_LINE

    lst = PyDict_GetItemStringWithError(special_registry, sel_getName(sel));
    if (lst == NULL) {
        goto error;
    }

    Py_INCREF(lst);

    /*
     * Look for the most specific match:
     * - class in the list item is either the class we're looking
     *   for, or the "closest" superclass. The list item class
     *   can be 'None', which is less specific than any other class.
     * - later items in the list with the same list item class
     *   are preferred over earlier items (those are metadata that
     *   was added later).
     */
    for (i = 0; i < PyList_GET_SIZE(lst); i++) {
        PyObject* entry   = PyList_GET_ITEM(lst, i);
        PyObject* pyclass = PyTuple_GET_ITEM(entry, 0);

        if (pyclass == NULL) // LCOV_BR_EXCL_LINE
            continue;        // LCOV_EXCL_LINE
        if (pyclass != Py_None
            && !PyType_IsSubtype((PyTypeObject*)search_class, (PyTypeObject*)pyclass)) {
            continue;
        }

        if (!special_class) {
            /* No match yet, use */
            special_class = pyclass;
            result        = PyTuple_GET_ITEM(entry, 1);

        } else if (pyclass == Py_None) {
            /* Already have a match, Py_None is less specific */
            continue;

        } else if (PyType_IsSubtype((PyTypeObject*)special_class,
                                    (PyTypeObject*)pyclass)) {
            /* special_type is a superclass of search_class,
             * but a subclass of the current match, hence it is
             * a more specific match or a simular match later in the
             * list.
             */
            special_class = pyclass;
            result        = PyTuple_GET_ITEM(entry, 1);
        }
    }
    Py_XDECREF(search_class);
    if (!result)
        goto error;

    return PyCapsule_GetPointer(result, "objc.__memblock__");

error:
    return NULL;
}

PyObjC_CallFunc _Nullable PyObjC_FindCallFunc(Class class, SEL sel)
{
    struct registry* special;

    PyObjC_Assert(special_registry != NULL, NULL);

    special = search_special(class, sel);
    if (special) {
        return special->call_to_objc;
    } else if (PyErr_Occurred()) {
        return NULL;
    }

    return PyObjCFFI_Caller;
}

static struct registry* _Nullable find_signature(const char* signature)
{
    PyObject* o;
    char      signature_buf[1024];
    int       res;

    res = PyObjCRT_SimplifySignature(signature, signature_buf, sizeof(signature_buf));
    if (res == -1) {
        PyErr_SetString(PyObjCExc_Error, "cannot simplify signature");
        return NULL;
    }

    if (signature_registry == NULL)
        return NULL;

    PyObject* key = PyBytes_FromString(signature_buf);
    if (key == NULL) { // LCOV_BR_EXCL_LINE
        return NULL;   // LCOV_EXCL_LINE
    }
    o = PyDict_GetItemWithError(signature_registry, key);
    Py_DECREF(key);
    if (o == NULL)
        return NULL;

    return PyCapsule_GetPointer(o, "objc.__memblock__");
}

extern IMP
PyObjC_MakeIMP(Class class, Class _Nullable super_class, PyObject* sel, PyObject* imp)
{
    struct registry*       generic;
    struct registry*       special;
    SEL                    aSelector = PyObjCSelector_GetSelector(sel);
    PyObjCFFI_ClosureFunc  func      = NULL;
    IMP                    retval;
    PyObjCMethodSignature* methinfo;

    if (super_class != nil) {
        special = search_special(super_class, aSelector);
        if (special) {
            func = special->call_to_python;
        } else if (PyErr_Occurred()) {
            return NULL;
        }
    }

    if (func == NULL) {
        const char* sel_signature = PyObjCSelector_Signature(sel);
        if (sel_signature == NULL) {
            return NULL;
        }
        generic = find_signature(sel_signature);
        if (generic != NULL) {
            func = generic->call_to_python;
        } else if (PyErr_Occurred()) {
            return NULL;
        }
    }

    if (func == PyObjCUnsupportedMethod_IMP) {
        PyErr_Format(PyExc_TypeError, "Implementing %s in Python is not supported",
                     sel_getName(aSelector));
        return NULL;
    }

    if (func != NULL) {
        const char* sel_signature = PyObjCSelector_Signature(sel);
        if (sel_signature == NULL) {
            return NULL;
        }
        methinfo = PyObjCMethodSignature_ForSelector(
            class, (PyObjCSelector_GetFlags(sel) & PyObjCSelector_kCLASS_METHOD) != 0,
            PyObjCSelector_GetSelector(sel), sel_signature,
            PyObjCNativeSelector_Check(sel));
        if (methinfo == NULL) {
            return NULL;
        }
        retval = PyObjCFFI_MakeClosure(methinfo, func, imp);
        if (retval != NULL) {
            Py_INCREF(imp);
        }
        Py_DECREF(methinfo);
        return retval;
    } else {
        PyErr_Clear();

        const char* sel_signature = PyObjCSelector_Signature(sel);
        if (sel_signature == NULL) {
            return NULL;
        }
        methinfo = PyObjCMethodSignature_ForSelector(
            class, (PyObjCSelector_GetFlags(sel) & PyObjCSelector_kCLASS_METHOD) != 0,
            PyObjCSelector_GetSelector(sel), sel_signature,
            PyObjCNativeSelector_Check(sel));
        if (methinfo == NULL) {
            return NULL;
        }
        retval = blockimpForSignature(PyObjCSelector_GetSelector(sel), sel_signature, imp,
                                      methinfo);
        if (retval != NULL) {
            return retval;
        }
        retval =
            PyObjCFFI_MakeIMPForSignature(methinfo, PyObjCSelector_GetSelector(sel), imp);
        Py_DECREF(methinfo);
        return retval;
    }
}

// LCOV_EXCL_START
/* The two functions below are never called */
void
PyObjCUnsupportedMethod_IMP(ffi_cif* cif __attribute__((__unused__)),
                            void* resp __attribute__((__unused__)), void** args,
                            void* userdata __attribute__((__unused__)))
{
    @throw [NSException
        exceptionWithName:NSInvalidArgumentException
                   reason:[NSString
                              stringWithFormat:
                                  @"Implementing %s from Python is not supported for %@",
                                  sel_getName(*(SEL*)args[1]), *(id*)args[0]]
                 userInfo:nil];
}

PyObject*
PyObjCUnsupportedMethod_Caller(PyObject* meth, PyObject* self,
                               PyObject* const* args __attribute__((__unused__)),
                               size_t           nargs __attribute__((__unused__)))
{
    PyErr_Format(PyExc_TypeError, "Cannot call '%s' on '%R' from Python",
                 sel_getName(PyObjCSelector_GetSelector(meth)), self);
    return NULL;
}
// LCOV_EXCL_STOP

NS_ASSUME_NONNULL_END
