# Logical Base Class -> Provides the API for logical updates and defers to a concrete subclass to implement the update themselves. 
# Also manages and storage locking and dereferencing internal nodes. 
# Value Ref a python object that is a reference eto a binary blob stored in database . The indirection let's us avoid loading the entire data store into memory all at once . 
