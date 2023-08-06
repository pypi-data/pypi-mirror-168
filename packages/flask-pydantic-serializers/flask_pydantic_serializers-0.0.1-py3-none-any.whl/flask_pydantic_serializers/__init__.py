from copy import deepcopy

from sqlalchemy import desc, func

# from providers.postgres import db_session
from helpers import query_manager as qm


class BaseCrud:
    """
    __model_kls__: Define the main postgres model to be used for the orm.
    __related_kls__: retrieve information if any related data needs to be created.
                  Eg. one_to_one=dict(<field_in_main_schema>=<Postgres_Model>)
    """
    __model_kls__ = None
    __related_kls__: dict = dict(
        one_to_one=dict(),
        one_to_many=dict(),
        many_to_many=dict(),
    )
    __serialize_when_none__: bool = False
    __by_alias_global__: bool = False

    def _get_validated_data(self):
        pydantic_kw: dict = dict(exclude_unset=True)
        if self.__serialize_when_none__:
            pydantic_kw.update(dict(exclude_none=False, exclude_unset=False))
        if self.__by_alias_global__:
            pydantic_kw.update(dict(by_alias=True))
        return self.dict(**pydantic_kw)

    def bulk_save(self):
        pass

    def update(self, filter_fields, **kwargs):
        """Provide fields/data to target the correct obj, preferable the id of obj.

        This update version can only handle 1-level deep updates.
        """
        # Need to handle if error occurs

        validated_data = self._get_validated_data()
        hold_data = deepcopy(validated_data)
        session = db_session()
        obj = session.query(self.__model_kls__).filter_by(**filter_fields).one()

        if not obj:
            return

        if "id" in validated_data:
            del validated_data["id"]

        one_to_one = self.__related_kls__.get("one_to_one", dict())
        one_to_many = self.__related_kls__.get("one_to_many", dict())
        many_to_many = self.__related_kls__.get("many_to_many", dict())

        # Handle updates targeting one-to-one or one-to-many
        for k, v in validated_data.items():
            def update_process(ctx):
                del hold_data[k]
                target_obj = getattr(obj, k)
                target_obj = target_obj.to_json(
                    rel=False) if target_obj else dict()

                linked_field = ctx["linked_field"]
                linked_model = ctx["model_kls"]

                # Related object does not exist, create
                if "id" not in target_obj:
                    target_obj.update(validated_data[k])
                    rel_obj = linked_model(**kwargs)
                    session.add(rel_obj)
                    session.commit()
                    setattr(obj, linked_field, rel_obj.id)

                elif "id" in target_obj:
                    rel_obj = qm.get_one(session, linked_model,
                                         dict(id=target_obj["id"]))
                    for key_, value_ in validated_data[k].items():
                        setattr(rel_obj, key_, value_)
                    session.add(rel_obj)

            if isinstance(v, dict) and (k in one_to_many or k in one_to_one):
                update_process(one_to_many.get(k) or one_to_one.get(k))

            elif isinstance(v, list) and k in many_to_many:
                obj = qm.update_many_to_many(
                    session=session,
                    sub_kls=many_to_many[k]["model_kls"],
                    obj=obj,
                    kwargs=v,
                    rel_field=k,
                )
                del hold_data[k]

        for k, v in hold_data.items():
            setattr(obj, k, v)

        session.add(obj)
        session.commit()

        return self._return_results(obj, **kwargs)

    def create(self, **kwargs):
        """Create new row under target model."""

        # Need to handle if error occurs
        validated_data = self._get_validated_data()
        if not validated_data:
            return None

        if "id" in validated_data:
            del validated_data["id"]

        session = db_session()

        one_to_one = self.__related_kls__.get("one_to_one", dict())
        one_to_many = self.__related_kls__.get("one_to_many", dict())
        many_to_many = self.__related_kls__.get("many_to_many", dict())

        one_to_one_data = dict()
        for related_field in one_to_one.keys():
            if validated_data.get(related_field):
                one_to_one_data[related_field] = validated_data[related_field]
                del validated_data[related_field]

        for related_field, val in one_to_many.items():
            if validated_data.get(related_field):
                data_ = validated_data[related_field]

                # Remove data from main parent data
                del validated_data[related_field]

                # Get or create the new object
                rel_model = val["model_kls"]
                rel_instance = session.query(rel_model).filter_by(
                    **data_).first()
                if not rel_instance:
                    rel_instance = rel_model(**data_)
                    session.add(rel_instance)
                    session.commit()
                # Link created rel_obj back to parent
                validated_data[val["linked_field"]] = rel_instance.id

        # Many-to-many should always be an input of lists of dictionaries.
        # The serializer will have a main_model and secondary model.
        # Also a linked_fields-list that is the two fields defined on the secondary model.
        many_to_many_link: list = list()
        for related_field, val in many_to_many.items():
            if validated_data.get(related_field):
                data_ = validated_data[related_field]

                # Remove data from main parent data
                del validated_data[related_field]

                # Get or create the new object
                rel_model = val["model_kls"]

                # Here we loop through each dictionary in the list.
                # each object is created, id stored, and then other linked field hold.
                for v in data_:

                    # Check first if exist.
                    rel_instance = session.query(rel_model).filter_by(
                        **v).first()
                    if not rel_instance:
                        rel_instance = rel_model(**v)
                        session.add(rel_instance)
                        session.commit()

                    # Get the two linked fields on defined on secondary model
                    first_field = val["linked_fields"][0]
                    second_field = val["linked_fields"][-1]
                    # Remember the one field later populated after main object created.
                    many_to_many_link.append(
                        {
                            "first_field": first_field,
                            second_field: rel_instance.id,
                            "model": val["second_kls"],
                        }
                    )

        # Main/Parent object created.
        obj_created = self.__model_kls__(**validated_data)
        # Need to commit at this point, some other related might need it.
        session.add(obj_created)

        session.commit()

        # One-to-one
        for field_, data in one_to_one_data.items():
            model_ = one_to_one[field_]["model_kls"]
            link_field = one_to_one[field_]["linked_field"]

            data[link_field] = obj_created.id
            instance = model_(**data)
            session.add(instance)

        # Many to Many
        for linked_data in many_to_many_link:
            field_ = linked_data["first_field"]
            link_model = linked_data["model"]

            del linked_data["first_field"]
            del linked_data["model"]

            linked_data[field_] = obj_created.id
            instance = link_model(**linked_data)
            session.add(instance)
        session.commit()
        return self._return_results(obj_created, **kwargs)

    def get_or_create(self, **kwargs):
        if not self.__model_kls__:
            return {}
        obj = self.get_obj(**kwargs)

        if obj:
            return obj

        return self.create(**kwargs)

    def get_obj(self, **kwargs):
        if not self.__model_kls__:
            return {}

        session = db_session()

        data = self._get_validated_data()
        if not data:
            return None

        if data.get("id"):
            obj = session.query(self.__model_kls__).filter_by(
                id=data.get("id")).first()
            return self._return_results(obj, **kwargs)

        data_ = deepcopy(data)
        for k, v in data.items():
            if isinstance(v, (tuple, list, dict)):
                del data_[k]
        obj = session.query(self.__model_kls__).filter_by(**data_).first()

        return self._return_results(obj, **kwargs)

    def get_obj_by_order(self, order_by: dict, **kwargs):
        """
        Given model class and parameters fetch data from db.
        order_by = {desc: True/False, field: name of field to order_by}
        """
        session = db_session()

        data = self._get_validated_data()
        data_ = deepcopy(data)
        for k, v in data.items():
            if isinstance(v, (tuple, list, dict)):
                del data_[k]

        q = session.query(self.__model_kls__).filter_by(**data_)

        if order_by.get("desc"):
            obj = q.order_by(desc(order_by["field"])).first()
        else:
            obj = q.order_by(order_by["field"]).first()

        return self._return_results(obj, **kwargs)

    def get_objects(self, **kwargs):
        # TODO: need to add support for order_by
        data = self._get_validated_data()
        session = db_session()

        if kwargs.get("count") is True:
            results = \
            session.query(func.count(self.__model_kls__.id)).filter_by(
                **data).one()[0]
            return results[0] if results else 0

        # if kwargs.get("get_in") is True:
        #     results = session.query(model_).filter_by(**data).all()
        #     .filter(~model_.ctrl_id.in_(all_insured_ctrl_ids))
        #     return results[0] if results else 0
        results = session.query(self.__model_kls__).filter_by(**data).all()
        return self._return_results(results, **kwargs)

    def hard_delete(self):
        session = db_session()

        data = self._get_validated_data()
        if not data:
            return None

        if data.get("id"):
            session.query(self.__model_kls__).filter_by(id=data["id"]).delete()
            session.commit()
            return

        data_ = deepcopy(data)
        for k, v in data.items():
            if isinstance(v, (tuple, list, dict)):
                del data_[k]

        obj = session.query(self.__model_kls__).filter_by(**data_).first()
        if obj:
            session.delete(obj)
            session.commit()

    def hard_delete_objects(self):
        session = db_session()

        data = self._get_validated_data()
        if not data:
            return None

        data_ = deepcopy(data)
        for k, v in data.items():
            if isinstance(v, (tuple, list, dict)):
                del data_[k]

        session.query(self.__model_kls__).filter_by(**data_).delete()
        session.commit()

    @staticmethod
    def _return_results(results, **kwargs):
        if not results:
            return results

        _include_hybrid = kwargs.get("_include_hybrid", False)
        _rel = kwargs.get("_rel", False)
        _return_dict = kwargs.get("_return_dict", True)
        if not _return_dict:
            return results

        if isinstance(results, list):
            return [
                result.to_json(include_hybrid=_include_hybrid, rel=_rel)
                for result in results
            ]

        return results.to_json(include_hybrid=_include_hybrid, rel=_rel)
