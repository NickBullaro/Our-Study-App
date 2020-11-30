class MockSession:
    '''
    class to be used in tests to mock models.DB.session and its subsequent calls
    '''
    def __init__(self):
        return
    
    class query:
        def init(self, dict_db):
            self.db = dict_db.copy()
            for key in self.db:
                self.db[key] = dict_db[key].copy()
        
        def filter_by(**kwargs):
            for column in kwargs:
                if column = 'id':
                    for row_id in self.db:
                        if kwargs[column] != row_id:
                            self.db.pop(row_id)
                else:
                    for row_id in self.db:
                        if column in self.db[row_id]:
                            if kwargs[column] != self.db[row_id][column]:
                                self.db.pop(row_id)
            return self
        
        def all(self):
            return self.db