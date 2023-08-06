import os
from typing import Any, Iterable, Optional
from collections import OrderedDict
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django import template


class FilterType:
    CONTAINS = "contains"
    ICONTAINS = "icontains"
    EXACT = "exact"
    IEXACT = "iexact"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    ISNULL = "isnull"
    STARTSWITH = "startswith"
    ISTARTSWITH = "istartswith"
    ENDSWITH = "endswith"
    IENDSWITH = "iendswith"
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    WEEK_DAY = "week_day"
    TIME = "time"
    DATE = "date"


class BaseRow:
    _creation_counter = 0

    def get_value(self, field, obj):
        """Get the value for a given field

        :param field: The field to get the value for
        :param obj: The object to get the value for
        :return: The value for the field
        :rtype: Any
        :raises: AttributeError if the field does not exist
        :raises: NotImplementedError if the attr is not implemented
        """
        raise NotImplementedError()


class Row(BaseRow):
    def __init__(
        self,
        name: Optional[str] = None,
        searchable: Optional[bool] = False,
        search_type: Optional[str] = FilterType.ICONTAINS,
        visible: Optional[bool] = True,
        auto_hide: Optional[bool] = False,
        orderable: Optional[bool] = False,
        datetime_format: Optional[str] = "%d/%m/%Y %H:%M",
        width: Optional[int] = 100,
        align: Optional[str] = "left",
    ) -> None:
        self.name = name
        self.searchable = searchable
        self.visible = visible
        self.search_type = search_type
        self.auto_hide = auto_hide
        self.orderable = orderable
        self.datetime_format = datetime_format
        self.width = width
        self.align = align

    def get_value(self, field, obj) -> Any:
        value = getattr(obj, field)

        if type(value) == datetime:
            value = value.strftime(self.datetime_format)

        return value


class RowMethod(BaseRow):
    def __init__(
        self,
        method: Optional[str] = None,
        name: Optional[str] = None,
        visible: Optional[bool] = True,
        searchable: Optional[bool] = True,
        search_value: Optional[str] = None,
        auto_hide: Optional[bool] = False,
        orderable: Optional[bool] = False,
        datetime_format: Optional[str] = "%d/%m/%Y %H:%M",
        width: Optional[int] = 100,
        align: Optional[str] = "left",
    ):
        self.name = name
        self.visible = visible
        self.searchable = searchable
        self.search_value = search_value
        self.method = method
        self.auto_hide = auto_hide
        self.orderable = orderable
        self.datetime_format = datetime_format
        self.width = width
        self.align = align

    def get_method_name(self, field: str) -> str:
        """Get the default method name for a given field if the user did not specify one

        :param field: The field to get the method name for
        :return: The method name for the field
        :rtype: str
        """
        return self.method or f"get_{field}"

    def get_value(self, field, obj) -> Any:
        value = getattr(self, self.get_method_name(field))(obj)

        if type(value) == datetime:
            value = value.strftime(self.datetime_format)

        return value


class RowChoice(BaseRow):
    def __init__(
        self,
        choices: Optional[Iterable[tuple]] = None,
        name: Optional[str] = None,
        searchable: Optional[bool] = False,
        search_type: Optional[str] = FilterType.ICONTAINS,
        visible: Optional[bool] = True,
        auto_hide: Optional[bool] = False,
        orderable: Optional[bool] = False,
        width: Optional[int] = 100,
        align: Optional[str] = "left",
    ) -> None:
        self.name = name
        self.searchable = searchable
        self.visible = visible
        self.search_type = search_type
        self.auto_hide = auto_hide
        self.orderable = orderable
        self.choices = choices
        self.width = width
        self.align = align

    def get_choice_label(self, value: str) -> str:
        """Get the label for a given choice value

        :param value: The value to get the label for
        :return: The label for the choice value
        :rtype: str
        """
        return next((choice[1] for choice in self.choices if choice[0] == value))

    def get_value(self, field, obj):
        value = getattr(obj, field)
        return value


class DatatableMetaclass(type):
    @classmethod
    def _get_declared_fields(cls, bases, attrs) -> OrderedDict:
        """Get the declared fields for the class"""
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, BaseRow)]

        fields.sort(key=lambda x: x[1]._creation_counter)

        known = set(attrs)

        def visit(name):
            known.add(name)
            return name

        base_fields = [
            (visit(name), f)
            for base in bases if hasattr(base, '_declared_fields')
            for name, f in base._declared_fields.items() if name not in known
        ]

        return OrderedDict(base_fields + fields)

    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = cls._get_declared_fields(bases, attrs)
        return super().__new__(cls, name, bases, attrs)


class Datatable(View, metaclass=DatatableMetaclass):
    model = None
    table_id = None
    template_name = "datatable/list.html"

    def __init__(self) -> None:
        self.validate_rows()

    class Meta:
        create_url_name = None
        delete_url_name = None
        update_url_name = None

        create_permission = None
        update_permission = None
        delete_permission = None

        sortable = False

    def get_columns(self) -> list:
        """Get the columns for the datatable

        :return: The columns for the datatable
        :rtype: list
        """
        columns = []

        for field, row in self._declared_fields.items():
            columns.append({
                "name": row.name or field,
                "field": field,
                "auto_hide": row.auto_hide,
                "sortable": row.orderable,
                "width": row.width,
                "align": row.align,
            })

        return columns

    def get_permissions(self) -> dict:
        """Get the permissions for the datatable

        :return: The permissions for the datatable
        :rtype: dict
        """
        user = self.request.user

        return {
            "can_create": user.has_perm(self.create_permission),
            "can_update": user.has_perm(self.update_permission),
            "can_delete": user.has_perm(self.delete_permission)
        }

    def get_extended_html_filepath(self) -> str:
        filepath = os.path.dirname(self.template_name)
        return os.path.join(filepath, f"html/{self.table_id}/index.js")

    def have_extended_functions(self) -> bool:
        """Check if the datatable has extended functions

        :return: True if the datatable has extended functions, False otherwise
        :rtype: bool
        """
        try:
            template.loader.get_template(self.get_extended_html_filepath())
            return True
        except template.TemplateDoesNotExist:
            return False

    def get_context_data(self, **kwargs) -> dict:
        """Get the context data for the datatable

        :param kwargs: Any extra context data to pass to the template
        :return: The context data for the datatable
        :rtype: dict
        """
        context = dict()

        context["table_id"] = self.table_id
        context["search_id"] = self.search_id
        context["columns"] = self.get_columns()
        context["permissions"] = self.get_permissions()
        context["sortable"] = getattr(self.Meta, "sortable", None)
        context["extend_js"] = self.have_extended_functions()
        context["extended_filepath"] = self.get_extended_html_filepath()

        if url := getattr(self.Meta, "create_url_name", None):
            context["create_url"] = reverse(url),

        return context

    def validate_rows(self):
        """Validate all the rows needed for the datatable to work

        :raises: AssertionError if a row is missing or invalid
        """
        assert self.model is not None, "model is not set"
        assert self.table_id is not None, "table_id is not set"
        meta = self.model._meta

        for field, row in self._declared_fields.items():
            if not type(row) == RowMethod:
                assert not type(row) == RowMethod and meta.get_field(field), \
                    "field {} is not in model {}".format(field, self.model)
            else:
                assert type(row) == RowMethod and getattr(self, row.get_method_name(field)), \
                    "field {} is not in model {}".format(field, self.model)

    def get_queryset(self) -> Iterable[Any]:
        """Get the queryset for the datatable

        :return: The queryset for the datatable
        :rtype: Iterable[Any]
        """
        filters, order_by = self.get_queryset_data()
        return self.model.objects.filter(filters).order_by(*order_by)

    def get_paginated_data(self) -> tuple:
        """Get the paginated data for the datatable
        TODO: Implement CustomPaginator

        :return: The paginated data for the datatable
        :rtype: tuple
        """
        queryset = self.get_queryset()
        search_data = self.get_search_data()
        paginator = Paginator(queryset, search_data.get("per_page"))
        page = paginator.get_page(search_data.get("page"))

        return page.object_list, paginator.num_pages, page.number, queryset.count()

    @property
    def search_id(self) -> str:
        """Get the search id for the datatable

        :return: The search id for the datatable
        :rtype: str
        """
        return f"kt_datatable_{self.table_id}_search"

    @property
    def create_permission(self) -> str:
        """Get the create permission for the datatable

        :return: The create permission for the datatable
        :rtype: str
        """
        default = "{}.add_{}".format(self.model._meta.app_label, self.model._meta.model_name)
        return getattr(self.Meta, "create_permission", None) or default

    @property
    def update_permission(self) -> str:
        """Get the update permission for the datatable

        :return: The update permission for the datatable
        :rtype: str
        """
        default = "{}.change_{}".format(self.model._meta.app_label, self.model._meta.model_name)
        return getattr(self.Meta, "update_permission", None) or default

    @property
    def delete_permission(self) -> str:
        """Get the delete permission for the datatable

        :return: The delete permission for the datatable
        :rtype: str
        """
        default = "{}.delete_{}".format(self.model._meta.app_label, self.model._meta.model_name)
        return getattr(self.Meta, "delete_permission", None) or default

    def get_meta_context(self, actual_page: int, total_pages: int, total_records: int) -> dict:
        """Get the meta context for the datatable

        :param actual_page: The actual page of the datatable
        :param total_pages: The total pages of the datatable
        :param total_records: The total records of the datatable
        :return: The meta context for the datatable
        :rtype: dict
        """
        search_data = self.get_search_data()

        return {
            "page": actual_page,
            "pages": total_pages,
            "perpage": search_data.get("per_page"),
            "total": total_records,
            "sort": search_data.get("sort"),
            "field": search_data.get("sort_field"),
        }

    def get_row_context(self, row, field, obj) -> dict:
        """Get the row context for the datatable, this will be returned
        when the datatable script requests the row data via POST

        :param row: The row for the datatable
        :param field: The field for the datatable
        :param obj: The object for the datatable
        :return: The row context for the datatable
        :rtype: dict
        """
        context = dict()
        value = row.get_value(field, obj)

        if type(row) == RowChoice:
            context[f"{field}_choice_label"] = row.get_choice_label(value)

        context.update({f"{field}_name": row.name or field})
        context.update({f"{field}_visible": row.visible})
        context.update({f"{field}_auto_hide": row.auto_hide})
        context.update({f"{field}_width": row.width})
        context.update({field: value})
        return context

    def get_row_data(self, obj) -> dict:
        """Get the row data for the datatable.

        :param obj: The object for the datatable
        :return: The row data for the datatable
        :rtype: dict
        """
        row_data = {"DT_RowId": obj.id}

        for field, row in self._declared_fields.items():
            row_data.update(self.get_row_context(row, field, obj))

        if url := getattr(self.Meta, "update_url_name", None):
            row_data.update({
                "update_url": reverse(url, kwargs={"pk": obj.pk})}
            )

        if url := getattr(self.Meta, "delete_url_name", None):
            row_data.update({
                "delete_url": reverse(url, kwargs={"pk": obj.pk})}
            )

        return row_data

    def get_data_context(self, object_list) -> list:
        """Get the data context for the datatable, this will be used in POST 
        requests called from the datatable

        :param object_list: The object list for the datatable
        :return: The data context for the datatable
        :rtype: list
        """
        return [self.get_row_data(obj) for obj in object_list]

    def process_response(self) -> dict:
        """Process the response for the datatable, call the needed methods to build
        the data structure needed to process the datatable. {data: [], meta: {}}

        :return: The response for the datatable
        :rtype: dict
        """
        object_list, total_pages, actual_page, total_records = self.get_paginated_data()
        meta = self.get_meta_context(actual_page, total_pages, total_records)
        data = self.get_data_context(object_list)
        return {"meta": meta, "data": data}

    def get_queryset_data(self) -> list:
        """Get the queryset data for the datatable. This function is generic and manages all
        the fields like a string (Unless you have defined the search_type like DATE types)

        :return: The queryset data for the datatable
        :rtype: list
        """
        search_data = self.get_search_data()
        filters = Q()
        order_by = []
        order_type = "" if search_data.get("sort", "desc") == "desc" else "-"

        for field, row in self._declared_fields.items():
            if type(row) == RowMethod:
                continue

            if row.searchable and search_data.get("query"):
                filters |= Q(**{f"{field}__{row.search_type}": search_data.get("query")})
            if row.orderable and field == search_data.get("sort_field"):
                order_by.append(f"{order_type}{field}")

        return filters, order_by

    def get_search_data(self) -> dict:
        """Get the search data from the request body. This data is suposed to be sent by
        the datatable script via POST request.

        :return: The search data from the request body
        :rtype: dict
        """
        return {
            "query": self.request.POST.get(f"query[{self.search_id}]"),
            "page": self.request.POST.get("pagination[page]"),
            "pages": self.request.POST.get("pagination[pages]"),
            "per_page": self.request.POST.get("pagination[perpage]"),
            "total": self.request.POST.get("pagination[total]"),
            "sort": self.request.POST.get("sort[sort]"),
            "sort_field": self.request.POST.get("sort[field]"),
        }

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Process the POST request for the datatable. This method is called by the datatable

        :param request: The request for the datatable
        :param args: The args for the datatable
        :param kwargs: The kwargs for the datatable
        :return: The response for the datatable
        :rtype: HttpResponse
        """
        response = self.process_response()
        return JsonResponse(response)

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Process the GET request for the datatable

        :param request: The request for the datatable
        :param args: The args for the datatable
        :param kwargs: The kwargs for the datatable
        :return: The response for the datatable
        :rtype: HttpResponse
        """
        return render(request, self.template_name, self.get_context_data())
