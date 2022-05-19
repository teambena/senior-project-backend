from app import BaseQuery, db
class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def _get_models(self):   
        if hasattr(BaseQuery, 'attr'):
            return [BaseQuery.attr.target_mapper]
        else:
            return self._mapper_zero().class_

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            
            modelclass = args[0].class_
            delete_column = getattr(modelclass, "__delete_column__") # get column name for date deleted
            
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            
            model_class = obj._get_models()
            delete_field = getattr(model_class, delete_column)

            # filter where date deleted is null
            return obj.filter(delete_field == None) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_), session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.deleted else None
