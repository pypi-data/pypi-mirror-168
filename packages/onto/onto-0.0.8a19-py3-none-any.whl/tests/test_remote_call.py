from typing import Type

import pytest

from onto.stateful_functions import StatefunProxy, make_call, do_init, do_method


@pytest.mark.asyncio
async def test_remote_call():

    from onto.domain_model import DomainModel

    class A(DomainModel):

        @classmethod
        async def do_classmethod(cls) -> None:
            print('classmethod')

        async def do_method(self) -> None:
            print("method")


    A.method_proxy(doc_id='foo')

    from onto.invocation_context import invocation_context_var
    from onto.invocation_context import InvocationContextEnum
    with invocation_context_var(InvocationContextEnum.STATEFUL_FUNCTIONS_INTERNAL):
        assert await A.initializer_proxy(doc_id='foo').do_classmethod() is None
        assert await A.method_proxy(doc_id='foo').do_method() is None


@pytest.mark.asyncio
async def test_sub_cls_initializer():

    from onto.domain_model import DomainModel
    from onto.attrs import attrs

    class Mammal(DomainModel):

        class Meta:
            collection_name = 'Mammal'

        name = attrs.string

        async def set_name(self, *, name: str):
            self.name = name


    class Dolphin(Mammal):

        async def set_name(self, *, name: str):
            self.name = f'ocean {name}'

    doc_id = 'dolphin-1'

    sub_cls_proxy: StatefunProxy = Dolphin.initializer_proxy(
        doc_id=doc_id,
    )

    function_call = sub_cls_proxy._get_invocation_value(
        f_name='new',
        _kwargs={
            'doc_id': doc_id,
            'name': 'dolphin one'
        }
    )

    class MockStorage:
        pass

    mock_storage = MockStorage()
    await do_init(Dolphin, method_call=function_call, storage=mock_storage)

    res_d = mock_storage.__d
    assert res_d == (f'{{"obj_type": "Dolphin", "doc_id": "{doc_id}", "doc_ref": "Mammal/{doc_id}", "name": "dolphin one"}}')

    sub_cls_method_proxy: StatefunProxy = Dolphin.method_proxy(
        doc_id=doc_id,
    )

    method_function_call = sub_cls_method_proxy._get_invocation_value(
        f_name='set_name',
        _kwargs={
            'name': 'dolphin 1'
        }
    )

    await do_method(
        obj_cls=Mammal,
        method_call=method_function_call,
        storage=mock_storage,
        doc_id=doc_id,
        should_persist=True
    )

    method_res_d = mock_storage.__d
    assert method_res_d == (f'{{"obj_type": "Dolphin", "doc_id": "{doc_id}", "doc_ref": "Mammal/{doc_id}", "name": "ocean dolphin 1"}}')


