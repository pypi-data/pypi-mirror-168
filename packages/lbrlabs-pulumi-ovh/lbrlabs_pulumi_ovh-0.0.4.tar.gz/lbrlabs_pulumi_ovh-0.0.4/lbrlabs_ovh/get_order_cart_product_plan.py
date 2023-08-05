# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs

__all__ = [
    'GetOrderCartProductPlanResult',
    'AwaitableGetOrderCartProductPlanResult',
    'get_order_cart_product_plan',
    'get_order_cart_product_plan_output',
]

@pulumi.output_type
class GetOrderCartProductPlanResult:
    """
    A collection of values returned by getOrderCartProductPlan.
    """
    def __init__(__self__, cart_id=None, catalog_name=None, id=None, plan_code=None, price_capacity=None, prices=None, product=None, product_name=None, product_type=None, selected_prices=None):
        if cart_id and not isinstance(cart_id, str):
            raise TypeError("Expected argument 'cart_id' to be a str")
        pulumi.set(__self__, "cart_id", cart_id)
        if catalog_name and not isinstance(catalog_name, str):
            raise TypeError("Expected argument 'catalog_name' to be a str")
        pulumi.set(__self__, "catalog_name", catalog_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if plan_code and not isinstance(plan_code, str):
            raise TypeError("Expected argument 'plan_code' to be a str")
        pulumi.set(__self__, "plan_code", plan_code)
        if price_capacity and not isinstance(price_capacity, str):
            raise TypeError("Expected argument 'price_capacity' to be a str")
        pulumi.set(__self__, "price_capacity", price_capacity)
        if prices and not isinstance(prices, list):
            raise TypeError("Expected argument 'prices' to be a list")
        pulumi.set(__self__, "prices", prices)
        if product and not isinstance(product, str):
            raise TypeError("Expected argument 'product' to be a str")
        pulumi.set(__self__, "product", product)
        if product_name and not isinstance(product_name, str):
            raise TypeError("Expected argument 'product_name' to be a str")
        pulumi.set(__self__, "product_name", product_name)
        if product_type and not isinstance(product_type, str):
            raise TypeError("Expected argument 'product_type' to be a str")
        pulumi.set(__self__, "product_type", product_type)
        if selected_prices and not isinstance(selected_prices, list):
            raise TypeError("Expected argument 'selected_prices' to be a list")
        pulumi.set(__self__, "selected_prices", selected_prices)

    @property
    @pulumi.getter(name="cartId")
    def cart_id(self) -> str:
        return pulumi.get(self, "cart_id")

    @property
    @pulumi.getter(name="catalogName")
    def catalog_name(self) -> Optional[str]:
        return pulumi.get(self, "catalog_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="planCode")
    def plan_code(self) -> str:
        """
        Product offer identifier
        """
        return pulumi.get(self, "plan_code")

    @property
    @pulumi.getter(name="priceCapacity")
    def price_capacity(self) -> str:
        return pulumi.get(self, "price_capacity")

    @property
    @pulumi.getter
    def prices(self) -> Sequence['outputs.GetOrderCartProductPlanPriceResult']:
        """
        Prices of the product offer
        """
        return pulumi.get(self, "prices")

    @property
    @pulumi.getter
    def product(self) -> str:
        return pulumi.get(self, "product")

    @property
    @pulumi.getter(name="productName")
    def product_name(self) -> str:
        """
        Name of the product
        """
        return pulumi.get(self, "product_name")

    @property
    @pulumi.getter(name="productType")
    def product_type(self) -> str:
        """
        Product type
        """
        return pulumi.get(self, "product_type")

    @property
    @pulumi.getter(name="selectedPrices")
    def selected_prices(self) -> Sequence['outputs.GetOrderCartProductPlanSelectedPriceResult']:
        """
        Selected Price according to capacity
        """
        return pulumi.get(self, "selected_prices")


class AwaitableGetOrderCartProductPlanResult(GetOrderCartProductPlanResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrderCartProductPlanResult(
            cart_id=self.cart_id,
            catalog_name=self.catalog_name,
            id=self.id,
            plan_code=self.plan_code,
            price_capacity=self.price_capacity,
            prices=self.prices,
            product=self.product,
            product_name=self.product_name,
            product_type=self.product_type,
            selected_prices=self.selected_prices)


def get_order_cart_product_plan(cart_id: Optional[str] = None,
                                catalog_name: Optional[str] = None,
                                plan_code: Optional[str] = None,
                                price_capacity: Optional[str] = None,
                                product: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrderCartProductPlanResult:
    """
    Use this data source to retrieve information of order cart product plan.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_ovh as ovh

    mycart = ovh.get_order_cart(ovh_subsidiary="fr",
        description="my cart")
    plan = ovh.get_order_cart_product_plan(cart_id=mycart.id,
        price_capacity="renew",
        product="cloud",
        plan_code="project")
    ```


    :param str cart_id: Cart identifier
    :param str catalog_name: Catalog name
    :param str plan_code: Product offer identifier
    :param str price_capacity: Capacity of the pricing (type of pricing)
    :param str product: Product
    """
    __args__ = dict()
    __args__['cartId'] = cart_id
    __args__['catalogName'] = catalog_name
    __args__['planCode'] = plan_code
    __args__['priceCapacity'] = price_capacity
    __args__['product'] = product
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('ovh:index/getOrderCartProductPlan:getOrderCartProductPlan', __args__, opts=opts, typ=GetOrderCartProductPlanResult).value

    return AwaitableGetOrderCartProductPlanResult(
        cart_id=__ret__.cart_id,
        catalog_name=__ret__.catalog_name,
        id=__ret__.id,
        plan_code=__ret__.plan_code,
        price_capacity=__ret__.price_capacity,
        prices=__ret__.prices,
        product=__ret__.product,
        product_name=__ret__.product_name,
        product_type=__ret__.product_type,
        selected_prices=__ret__.selected_prices)


@_utilities.lift_output_func(get_order_cart_product_plan)
def get_order_cart_product_plan_output(cart_id: Optional[pulumi.Input[str]] = None,
                                       catalog_name: Optional[pulumi.Input[Optional[str]]] = None,
                                       plan_code: Optional[pulumi.Input[str]] = None,
                                       price_capacity: Optional[pulumi.Input[str]] = None,
                                       product: Optional[pulumi.Input[str]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOrderCartProductPlanResult]:
    """
    Use this data source to retrieve information of order cart product plan.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_ovh as ovh

    mycart = ovh.get_order_cart(ovh_subsidiary="fr",
        description="my cart")
    plan = ovh.get_order_cart_product_plan(cart_id=mycart.id,
        price_capacity="renew",
        product="cloud",
        plan_code="project")
    ```


    :param str cart_id: Cart identifier
    :param str catalog_name: Catalog name
    :param str plan_code: Product offer identifier
    :param str price_capacity: Capacity of the pricing (type of pricing)
    :param str product: Product
    """
    ...
