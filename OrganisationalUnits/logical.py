# Logical Base Class -> Provides the API for logical updates and defers to a concrete subclass to implement the update themselves. 
# Also manages and storage locking and dereferencing internal nodes. 
# Value Ref a python object that is a reference eto a binary blob stored in database . The indirection let's us avoid loading the entire data store into memory all at once . 

class LogicalBase(object):
    def __init__(self) -> None:
        self._storage = None
        self._tree_ref = None
    def get(self, key):
        if not self._storage.locked:
            self._refresh_tree_ref()
        return self._get(self._follow(self._tree_ref), key)
    
    def _refresh_tree_ref(self):
        self._tree_ref = self.node_ref_class(
            address=self._storage.get_root_address())
        
    def set(self, key, value):
        if self._storage.lock():
            self._refresh_tree_ref()
        self._tree_ref = self._insert(
            self._follow(self._tree_ref), key, self.value_ref_class(value))
        

    def commit(self):
        self._tree_ref.store(self._storage)
        self._storage.commit_root_address(self._tree_ref.address)


class ValueRef(object):
    def store(self, storage):
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_string(self._referent))

    def store(self, storage):
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_string(self._referent))
