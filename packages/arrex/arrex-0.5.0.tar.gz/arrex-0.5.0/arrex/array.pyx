
cdef class typedarray:

	cdef void *ptr
	cdef size_t dims
	cdef size_t *shape
	cdef ssize_t *strides
	
	cdef DDType dtype
	cdef readonly owner
	
	@property
	def shape(self):
		''' number of element along each dimension '''
		cdef typedlist shape = typedlist.__new__()
		shape.ptr = self.shape
		shape.size = shape.allocated = self.dims*sizeof(size_t)
		shape.dtype = declared('N')
		shape.owner = self
		
	@property
	def strides(self):
		''' byte offset between elements along each dimension '''
		cdef typedlist shape = typedlist.__new__()
		shape.ptr = self.strides
		shape.size = shape.allocated = self.dims*sizeof(ssize_t)
		shape.dtype = declared('n')
		shape.owner = self
	
	@property
	def dtype(self):
		''' the python dtype object, or the ddtype if there is not dtype '''
		return self.dtype.key or self.dtype
		
	@property
	def ddtype(self):
		''' the declaration of the dtype, a DDType instance '''
		return self.dtype
	
	def __init__(self, buffer, shape, strides, dtype=None):
		assert len(shape) == len(strides)
		self.dims = len(shape)
		self.shape = <size_t*> PyMem_Malloc(2*self.dims*sizeof(size_t))
		self.strides = self.shape + self.dims
		self.dtype = declared(dtype)
		self.owner = buffer

		indev()
		
	def __del__(self):
		PyMem_Free(self.shape)
		self.shape = 0
		self.strides = 0
		
	cdef object _getitem(self, void* place):
		return self.dtype.c_unpack(self.dtype, place)
		
	cdef int _setitem(self, void* place, obj) except -1:
		return self.dtype.c_pack(self.dtype, place, obj)
		
	
	def __len__(self):
		if self.dims:
			return self.shape[0]
		else:
			return 0
	
	def __getitem__(self, *index):
		
		# try to extract a simple element
		# indices must all be int and there must be as many indices as there is dimensions
		if len(index) == self.dims:
			for i in range(len(index)):
				if PyNumber_Check(index[i]):
					if index[i] < 0 or self.shape[i] <= index[i]:
						raise IndexError('index out of range for dimension {}'.format(i))
					ptr += index[i] * self.strides[i]
				else:
					break
			else:
				return self._getitem(ptr)
		
		# else get a slice array
		cdef ssize_t i
		cdef Py_ssize_t start, stop, step
		cdef typedarray new = typedarray.__new__()
		
		new.dims = 0
		new.ptr = self.ptr
		new.shape = <size_t> PyMem_Malloc(2*self.dims*sizeof(size_t))
		new.strides = new.shape + self.dims
		new.dtype = self.dtype
		new.owner = self.owner
		
		cdef size_t indices = len(index)
		for i in range(self.dims):
			if i < len(index):
				if PyNumber_Check(index[i]):
					new.ptr += index[i] * self.strides[i]
				elif isinstance(index[i], slice):
					if PySlice_Unpack(index[i], &start, &stop, &step):
						raise IndexError('incorrect slice')
					PySlice_AdjustIndices(self.shape[i], &start, &stop, step)
					
					new.strides[dims] = self.strides[i] * step
					new.shape[dims] = stop - start
					new.ptr += start * self.strides[i]
					new.dims += 1
			else:
				new.strides[dims] = self.strides[i]
				new.shape[dims] = self.shape[i]
				new.dims += 1
				
		return new
		
			
		
	def __setitem__(self, index, value):
		indev()
		
	def __iter__(self):
		indev()
	
	def transpose(self, reindex=None):
		indev()
		
	def ravel(self, dims=None):
		indev()
		
	def reshape(self, shape):
		indev()
		
	def extract(self, indices):
		indev()
		
	def swap(self, other):
		indev()
	
	
	def __eq__(self, other):
		indev()
		
	def index(self, value):
		indev()
	
	
	def __copy__(self):
		indev()
		
	def __deepcopy__(self):
		indev()
	
	
