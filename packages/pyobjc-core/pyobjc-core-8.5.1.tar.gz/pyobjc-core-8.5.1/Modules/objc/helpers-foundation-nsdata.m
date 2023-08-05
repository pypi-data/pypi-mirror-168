#include "pyobjc.h"

NS_ASSUME_NONNULL_BEGIN

static PyObject* _Nullable call_NSData_bytes(PyObject* method, PyObject* self,
                                             PyObject* const* arguments
                                             __attribute__((__unused__)),
                                             size_t nargs)
{
    const void*       bytes;
    NSUInteger        bytes_len;
    struct objc_super super;
    Py_buffer         info;

    if (PyObjC_CheckArgCount(method, 0, 0, nargs) == -1)
        return NULL;

    Py_BEGIN_ALLOW_THREADS
        @try {
            super.super_class = PyObjCSelector_GetClass(method);
            super.receiver    = PyObjCObject_GetObject(self);
            bytes             = ((void* (*)(struct objc_super*, SEL))objc_msgSendSuper)(
                &super, PyObjCSelector_GetSelector(method));
            bytes_len = ((NSUInteger(*)(struct objc_super*, SEL))objc_msgSendSuper)(
                &super, @selector(length));

        } @catch (NSObject* localException) {
            PyObjCErr_FromObjC(localException);
            bytes     = NULL;
            bytes_len = 0;
        }
    Py_END_ALLOW_THREADS

    if (bytes == NULL && PyErr_Occurred())
        return NULL;

    if (bytes == NULL) {
        /* Creating a memory view with a NULL pointer will
         * fail in 3.4 (and possibly earlier), use a
         * bytes object instead.
         */
        return PyBytes_FromStringAndSize("", 0);
    }

    if (PyBuffer_FillInfo( // LCOV_BR_EXCL_LINE
            &info, self, (void*)bytes, bytes_len, 1, PyBUF_FULL_RO)
        < 0) {
        return NULL; // LCOV_EXCL_LINE
    }
    return PyMemoryView_FromBuffer(&info);
}

static void
imp_NSData_bytes(ffi_cif* cif __attribute__((__unused__)), void* resp, void** args,
                 void* callable)
{
    id self = *(id*)args[0];
    // SEL _meth = *(SEL*)args[1];
    void** pretval = (void**)resp;

    PyObject* result;
    PyObject* pyself = NULL;
    int       cookie = 0;

    PyGILState_STATE state = PyGILState_Ensure();

    pyself = PyObjCObject_NewTransient(self, &cookie);
    if (pyself == NULL)
        goto error;

    PyObject* arglist[2] = {NULL, pyself};

    result = PyObject_Vectorcall((PyObject*)callable, arglist + 1,
                                 1 | PY_VECTORCALL_ARGUMENTS_OFFSET, NULL);
    PyObjCObject_ReleaseTransient(pyself, cookie);
    pyself = NULL;
    if (result == NULL)
        goto error;

    if (result == Py_None) {
        *pretval = NULL;
        Py_DECREF(result);
        PyGILState_Release(state);
        return;
    }

    {
        OCReleasedBuffer* temp = [[OCReleasedBuffer alloc] initWithPythonBuffer:result
                                                                       writable:NO];
        if (temp == nil) {
            *pretval = NULL;
            goto error;
        }
        [temp autorelease];
        *pretval = [temp buffer];
        PyGILState_Release(state);
    }
    return;

error:
    PyObjCErr_ToObjCWithGILState(&state);
    *pretval = NULL;
}

static PyObject* _Nullable call_NSMutableData_mutableBytes(PyObject*        method,
                                                           PyObject*        self,
                                                           PyObject* const* arguments
                                                           __attribute__((__unused__)),
                                                           size_t nargs)
{
    void*             bytes;
    NSUInteger        bytes_len;
    PyObject*         result;
    struct objc_super super;
    Py_buffer         info;

    if (PyObjC_CheckArgCount(method, 0, 0, nargs) == -1)
        return NULL;

    Py_BEGIN_ALLOW_THREADS
        @try {
            super.super_class = PyObjCSelector_GetClass(method);
            super.receiver    = PyObjCObject_GetObject(self);

            bytes = ((void* (*)(struct objc_super*, SEL))objc_msgSendSuper)(
                &super, PyObjCSelector_GetSelector(method));
            bytes_len = ((NSUInteger(*)(struct objc_super*, SEL))objc_msgSendSuper)(
                &super, @selector(length));

        } @catch (NSObject* localException) {
            PyObjCErr_FromObjC(localException);
            result    = NULL;
            bytes     = NULL;
            bytes_len = 0;
        }
    Py_END_ALLOW_THREADS

    if (bytes == NULL && PyErr_Occurred())
        return NULL;

    if (bytes == NULL) {
        /* XXX: Requires a custom NSData subclass for to test */
        /* The selector may return NULL for empty buffers,
         * return an empty memoryview.
         *
         * XXX: The Foundation headers in the 12.1 SDK say
         *      this selector is not nullable, and hence should
         *      never by NULL.
         */
        return PyMemoryView_FromMemory("", 0, PyBUF_WRITE);
    }

    if (PyBuffer_FillInfo( // LCOV_BR_EXCL_LINE
            &info, self, bytes, bytes_len, 0, PyBUF_FULL)
        < 0) {
        return NULL; // LCOV_EXCL_LINE
    }
    result = PyMemoryView_FromBuffer(&info);

    return result;
}

static void
imp_NSMutableData_mutableBytes(ffi_cif* cif __attribute__((__unused__)), void* resp,
                               void** args, void* callable)
{
    id self = *(id*)args[0];
    // SEL _meth = *(SEL*)args[1];
    void**    pretval = (void**)resp;
    PyObject* result;
    PyObject* pyself = NULL;
    int       cookie = 0;

    PyGILState_STATE state = PyGILState_Ensure();

    pyself = PyObjCObject_NewTransient(self, &cookie);
    if (pyself == NULL)
        goto error;

    PyObject* arglist[2] = {NULL, pyself};
    result               = PyObject_Vectorcall((PyObject*)callable, arglist + 1,
                                               1 | PY_VECTORCALL_ARGUMENTS_OFFSET, NULL);
    PyObjCObject_ReleaseTransient(pyself, cookie);
    pyself = NULL;
    if (result == NULL)
        goto error;

    if (result == Py_None) {
        *pretval = NULL;
        Py_DECREF(result);
        PyGILState_Release(state);
        return;
    }

    OCReleasedBuffer* temp = [[OCReleasedBuffer alloc] initWithPythonBuffer:result
                                                                   writable:YES];
    if (temp == nil) {
        *pretval = NULL;
        goto error;
    }
    [temp autorelease];
    *pretval = [temp buffer];
    PyGILState_Release(state);
    return;

error:
    *pretval = NULL;
    PyObjCErr_ToObjCWithGILState(&state);
}

int
PyObjC_setup_nsdata(void)
{
    Class classNSData        = objc_lookUpClass("NSData");
    Class classNSMutableData = objc_lookUpClass("NSMutableData");

    if (classNSData != NULL) { // LCOV_BR_EXCL_LINE

        if (PyObjC_RegisterMethodMapping( // LCOV_BR_EXCL_LINE
                classNSData, @selector(bytes), call_NSData_bytes, imp_NSData_bytes)
            < 0) {
            return -1; // LCOV_EXCL_LINE
        }
    }

    if (classNSMutableData != NULL) { // LCOV_BR_EXCL_LINE

        if (PyObjC_RegisterMethodMapping( // LCOV_BR_EXCL_LINE
                classNSMutableData, @selector(mutableBytes),
                call_NSMutableData_mutableBytes, imp_NSMutableData_mutableBytes)
            < 0) {
            return -1; // LCOV_EXCL_LINE
        }
    }

    return 0;
}

NS_ASSUME_NONNULL_END
