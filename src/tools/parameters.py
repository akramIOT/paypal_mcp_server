"""
Parameter definitions for the PayPal MCP server tools.

This module provides Pydantic models for all the parameters used by the
PayPal MCP server tools.
"""

from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field


# === INVOICE PARAMETERS ===

class CurrencyCode(str, Enum):
    """Currency code enumeration."""
    USD = "USD"


class UnitAmount(BaseModel):
    """Unit amount model."""
    currency_code: str = Field(..., description="Currency code of the unit amount")
    value: str = Field(..., description="The unit price. Up to 2 decimal points")


class Tax(BaseModel):
    """Tax model."""
    name: Optional[str] = Field(None, description="Tax name")
    percent: Optional[str] = Field(None, description="Tax Percent")


class UnitOfMeasure(str, Enum):
    """Unit of measure enumeration."""
    QUANTITY = "QUANTITY"
    HOURS = "HOURS"
    AMOUNT = "AMOUNT"


class InvoiceItem(BaseModel):
    """Invoice item model."""
    name: str = Field(..., description="The name of the item")
    quantity: str = Field(
        ..., 
        description="The quantity of the item that the invoicer provides to the payer. Value is from -1000000 to 1000000. Supports up to five decimal places. Cast to string"
    )
    unit_amount: UnitAmount = Field(..., description="Unit amount object")
    tax: Optional[Tax] = Field(None, description="Tax object")
    unit_of_measure: Optional[UnitOfMeasure] = Field(None, description="The unit of measure for the invoiced item")


class InvoiceDetail(BaseModel):
    """Invoice detail model."""
    invoice_date: Optional[str] = Field(None, description="The invoice date in YYYY-MM-DD format")
    currency_code: str = Field(..., description="Currency code of the invoice")


class InvoicerName(BaseModel):
    """Invoicer name model."""
    given_name: Optional[str] = Field(None, description="Given name of the invoicer")
    surname: Optional[str] = Field(None, description="Surname of the invoicer")


class Invoicer(BaseModel):
    """Invoicer model."""
    business_name: str = Field(..., description="Business name of the invoicer")
    name: InvoicerName = Field(..., description="Name of the invoicer")
    email_address: Optional[str] = Field(None, description="Email address of the invoicer")


class RecipientName(BaseModel):
    """Recipient name model."""
    given_name: Optional[str] = Field(None, description="Given name of the recipient")
    surname: Optional[str] = Field(None, description="Surname of the recipient")


class BillingInfo(BaseModel):
    """Billing information model."""
    name: Optional[RecipientName] = Field(None, description="Name of the recipient")
    email_address: Optional[str] = Field(None, description="Email address of the recipient")


class Recipient(BaseModel):
    """Recipient model."""
    billing_info: Optional[BillingInfo] = Field(None, description="The billing information of the invoice recipient")


class CreateInvoiceParameters(BaseModel):
    """Parameters for creating an invoice."""
    detail: InvoiceDetail = Field(..., description="The invoice detail")
    invoicer: Optional[Invoicer] = Field(None, description="The invoicer business information that appears on the invoice")
    primary_recipients: Optional[List[Recipient]] = Field(None, description="Array of recipients")
    items: Optional[List[InvoiceItem]] = Field(None, description="Array of invoice line items")


class GetInvoiceParameters(BaseModel):
    """Parameters for retrieving an invoice."""
    invoice_id: str = Field(..., description="The ID of the invoice to retrieve")


class ListInvoicesParameters(BaseModel):
    """Parameters for listing invoices."""
    page: Optional[int] = Field(1, description="The page number of the result set to fetch")
    page_size: Optional[int] = Field(100, description="The number of records to return per page (maximum 100)")
    total_required: Optional[bool] = Field(None, description="Indicates whether the response should include the total count of items")


class SendInvoiceParameters(BaseModel):
    """Parameters for sending an invoice."""
    invoice_id: str = Field(..., description="The ID of the invoice to send")
    note: Optional[str] = Field(None, description="A note to the recipient")
    send_to_recipient: Optional[bool] = Field(None, description="Indicates whether to send the invoice to the recipient")
    additional_recipients: Optional[List[str]] = Field(None, description="Additional email addresses to which to send the invoice")


class SendInvoiceReminderParameters(BaseModel):
    """Parameters for sending an invoice reminder."""
    invoice_id: str = Field(..., description="The ID of the invoice for which to send a reminder")
    subject: Optional[str] = Field(None, description="The subject of the reminder email")
    note: Optional[str] = Field(None, description="A note to the recipient")
    additional_recipients: Optional[List[str]] = Field(None, description="Additional email addresses to which to send the reminder")


class CancelSentInvoiceParameters(BaseModel):
    """Parameters for canceling a sent invoice."""
    invoice_id: str = Field(..., description="The ID of the invoice to cancel")
    note: Optional[str] = Field(None, description="A cancellation note to the recipient")
    send_to_recipient: Optional[bool] = Field(None, description="Indicates whether to send the cancellation to the recipient")
    additional_recipients: Optional[List[str]] = Field(None, description="Additional email addresses to which to send the cancellation")


class GenerateInvoiceQrCodeParameters(BaseModel):
    """Parameters for generating an invoice QR code."""
    invoice_id: str = Field(..., description="The invoice ID to generate QR code for")
    width: int = Field(..., description="The QR code width")
    height: int = Field(..., description="The QR code height")


# === PRODUCT PARAMETERS ===

class ProductType(str, Enum):
    """Product type enumeration."""
    PHYSICAL = "PHYSICAL"
    DIGITAL = "DIGITAL"
    SERVICE = "SERVICE"


class CreateProductParameters(BaseModel):
    """Parameters for creating a product."""
    name: str = Field(..., description="The product name")
    type: ProductType = Field(..., description="The product type")
    description: Optional[str] = Field(None, description="The product description")
    category: Optional[str] = Field(None, description="The product category")
    image_url: Optional[str] = Field(None, description="The image URL for the product")
    home_url: Optional[str] = Field(None, description="The home page URL for the product")


class ListProductsParameters(BaseModel):
    """Parameters for listing products."""
    page: Optional[int] = Field(None, description="The page number of the result set to fetch")
    page_size: Optional[int] = Field(None, description="The number of records to return per page (maximum 100)")
    total_required: Optional[bool] = Field(None, description="Indicates whether the response should include the total count of products")


class ShowProductDetailsParameters(BaseModel):
    """Parameters for retrieving product details."""
    product_id: str = Field(..., description="The ID of the product to show details for")


class UpdateProductParameters(BaseModel):
    """Parameters for updating a product."""
    product_id: str = Field(..., description="The ID of the product to update")
    operations: List[Dict] = Field(..., description="The PATCH operations to perform on the product")


# === SUBSCRIPTION PLAN PARAMETERS ===

class IntervalUnit(str, Enum):
    """Interval unit enumeration."""
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


class Frequency(BaseModel):
    """Frequency model."""
    interval_unit: IntervalUnit = Field(..., description="The unit of time for the billing cycle")
    interval_count: int = Field(..., description="The number of units for the billing cycle")


class FixedPrice(BaseModel):
    """Fixed price model."""
    currency_code: CurrencyCode = Field(..., description="The currency code for the fixed price")
    value: str = Field(..., description="The value of the fixed price")


class PricingScheme(BaseModel):
    """Pricing scheme model."""
    fixed_price: Optional[FixedPrice] = Field(None, description="The fixed price for the subscription plan")
    version: Optional[str] = Field(None, description="The version of the pricing scheme")


class TenureType(str, Enum):
    """Tenure type enumeration."""
    REGULAR = "REGULAR"
    TRIAL = "TRIAL"


class BillingCycle(BaseModel):
    """Billing cycle model."""
    frequency: Frequency = Field(..., description="The frequency of the billing cycle")
    tenure_type: TenureType = Field(..., description="The type of billing cycle tenure")
    sequence: int = Field(..., description="The sequence of the billing cycle")
    total_cycles: Optional[int] = Field(None, description="The total number of cycles in the billing plan")
    pricing_scheme: PricingScheme = Field(..., description="The pricing scheme for the billing cycle")


class SetupFee(BaseModel):
    """Setup fee model."""
    currency_code: Optional[CurrencyCode] = Field(None, description="The currency code for the setup fee")
    value: Optional[str] = Field(None, description="The value of the setup fee")


class SetupFeeFailureAction(str, Enum):
    """Setup fee failure action enumeration."""
    CONTINUE = "CONTINUE"
    CANCEL = "CANCEL"


class PaymentPreferences(BaseModel):
    """Payment preferences model."""
    auto_bill_outstanding: Optional[bool] = Field(None, description="Indicates whether to automatically bill outstanding amounts")
    setup_fee: Optional[SetupFee] = Field(None, description="The setup fee for the subscription plan")
    setup_fee_failure_action: Optional[SetupFeeFailureAction] = Field(None, description="The action to take if the setup fee payment fails")
    payment_failure_threshold: Optional[int] = Field(None, description="The number of failed payments before the subscription is canceled")


class Taxes(BaseModel):
    """Taxes model."""
    percentage: Optional[str] = Field(None, description="The tax percentage")
    inclusive: Optional[bool] = Field(None, description="Indicates whether the tax is inclusive")


class CreateSubscriptionPlanParameters(BaseModel):
    """Parameters for creating a subscription plan."""
    product_id: str = Field(..., description="The ID of the product for which to create the plan")
    name: str = Field(..., description="The subscription plan name")
    description: Optional[str] = Field(None, description="The subscription plan description")
    billing_cycles: List[BillingCycle] = Field(..., description="The billing cycles of the plan")
    payment_preferences: Optional[PaymentPreferences] = Field(None, description="The payment preferences for the subscription plan")
    taxes: Optional[Taxes] = Field(None, description="The tax details")


class ListSubscriptionPlansParameters(BaseModel):
    """Parameters for listing subscription plans."""
    product_id: Optional[str] = Field(None, description="The ID of the product for which to get subscription plans")
    page: Optional[int] = Field(None, description="The page number of the result set to fetch")
    page_size: Optional[int] = Field(None, description="The number of records to return per page (maximum 100)")
    total_required: Optional[bool] = Field(None, description="Indicates whether the response should include the total count of plans")


class ShowSubscriptionPlanDetailsParameters(BaseModel):
    """Parameters for retrieving subscription plan details."""
    plan_id: str = Field(..., description="The ID of the subscription plan to show")


# === SUBSCRIPTION PARAMETERS ===

class Name(BaseModel):
    """Name model."""
    given_name: str = Field(..., description="The subscriber given name")
    surname: Optional[str] = Field(None, description="The subscriber last name")


class CountryCode(str, Enum):
    """Country code enumeration."""
    US = "US"


class Address(BaseModel):
    """Address model."""
    address_line_1: str = Field(..., description="The first line of the address")
    address_line_2: Optional[str] = Field(None, description="The second line of the address")
    admin_area_1: str = Field(..., description="The city or locality")
    admin_area_2: str = Field(..., description="The state or province")
    postal_code: str = Field(..., description="The postal code")
    country_code: CountryCode = Field(..., description="The country code")


class ShippingAddress(BaseModel):
    """Shipping address model."""
    name: Name = Field(..., description="The subscriber shipping address name")
    address: Address = Field(..., description="The shipping address")


class PayerSelected(str, Enum):
    """Payer selected enumeration."""
    PAYPAL = "PAYPAL"
    CREDIT_CARD = "CREDIT_CARD"


class PayeePreferred(str, Enum):
    """Payee preferred enumeration."""
    IMMEDIATE_PAYMENT_REQUIRED = "IMMEDIATE_PAYMENT_REQUIRED"
    INSTANT_FUNDING_SOURCE = "INSTANT_FUNDING_SOURCE"


class PaymentMethod(BaseModel):
    """Payment method model."""
    payer_selected: PayerSelected = Field(..., description="The payment method selected by the payer")
    payee_preferred: Optional[PayeePreferred] = Field(None, description="The preferred payment method for the payee")


class ShippingAmount(BaseModel):
    """Shipping amount model."""
    currency_code: CurrencyCode = Field(..., description="The currency code for the shipping amount")
    value: str = Field(..., description="The value of the shipping amount")


class Subscriber(BaseModel):
    """Subscriber model."""
    name: Name = Field(..., description="The subscriber name")
    email_address: str = Field(..., description="The subscriber email address")
    shipping_address: Optional[ShippingAddress] = Field(None, description="The subscriber shipping address")


class ShippingPreference(str, Enum):
    """Shipping preference enumeration."""
    SET_PROVIDED_ADDRESS = "SET_PROVIDED_ADDRESS"
    GET_FROM_FILE = "GET_FROM_FILE"


class UserAction(str, Enum):
    """User action enumeration."""
    SUBSCRIBE_NOW = "SUBSCRIBE_NOW"
    CONTINUE = "CONTINUE"


class ApplicationContext(BaseModel):
    """Application context model."""
    brand_name: str = Field(..., description="The brand name")
    locale: Optional[str] = Field(None, description="The locale for the subscription")
    shipping_preference: Optional[ShippingPreference] = Field(None, description="The shipping preference")
    user_action: Optional[UserAction] = Field(None, description="The user action")
    return_url: str = Field(..., description="The return URL after the subscription is created")
    cancel_url: str = Field(..., description="The cancel URL if the user cancels the subscription")
    payment_method: PaymentMethod = Field(..., description="The payment method details")


class CreateSubscriptionParameters(BaseModel):
    """Parameters for creating a subscription."""
    plan_id: str = Field(..., description="The ID of the subscription plan to create")
    quantity: Optional[int] = Field(None, description="The quantity of the product in the subscription")
    shipping_amount: Optional[ShippingAmount] = Field(None, description="The shipping amount for the subscription")
    subscriber: Subscriber = Field(..., description="The subscriber details")
    application_context: Optional[ApplicationContext] = Field(None, description="The application context for the subscription")


class ShowSubscriptionDetailsParameters(BaseModel):
    """Parameters for retrieving subscription details."""
    subscription_id: str = Field(..., description="The ID of the subscription to show details")


class CancellationReason(BaseModel):
    """Cancellation reason model."""
    reason: str = Field(..., description="The reason for the cancellation of a subscription")


class CancelSubscriptionParameters(BaseModel):
    """Parameters for canceling a subscription."""
    subscription_id: str = Field(..., description="The ID of the subscription to cancel")
    payload: CancellationReason = Field(..., description="Payload for subscription cancellation")


# === SHIPMENT PARAMETERS ===

class ShipmentStatus(str, Enum):
    """Shipment status enumeration."""
    ON_HOLD = "ON_HOLD"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class CreateShipmentParameters(BaseModel):
    """Parameters for creating a shipment."""
    order_id: Optional[str] = Field(None, description="The ID of the order for which to create a shipment")
    tracking_number: str = Field(..., description="The tracking number for the shipment. ID is provided by the shipper. This is required to create a shipment")
    transaction_id: str = Field(..., description="The transaction ID associated with the shipment. Transaction ID available after the order is paid or captured. This is required to create a shipment")
    status: Optional[ShipmentStatus] = Field(ShipmentStatus.SHIPPED, description="The status of the shipment")
    carrier: Optional[str] = Field(None, description="The carrier handling the shipment")


class GetShipmentTrackingParameters(BaseModel):
    """Parameters for retrieving shipment tracking."""
    order_id: Optional[str] = Field(None, description="The ID of the order for which to create a shipment")
    transaction_id: Optional[str] = Field(None, description="The transaction ID associated with the shipment tracking to retrieve")


# === ORDER PARAMETERS ===

class OrderItem(BaseModel):
    """Order item model."""
    name: str = Field(..., description="The name of the item")
    quantity: Optional[int] = Field(1, description="The item quantity. Must be a whole number")
    description: Optional[str] = Field(None, description="The detailed item description")
    itemCost: float = Field(..., description="The cost of each item - up to 2 decimal points")
    taxPercent: Optional[float] = Field(0, description="The tax percent for the specific item")
    itemTotal: float = Field(..., description="The total cost of this line item")


class ShippingAddressOrder(BaseModel):
    """Shipping address model for orders."""
    address_line_1: Optional[str] = Field(None, description="The first line of the address, such as number and street, for example, `173 Drury Lane`. This field needs to pass the full address")
    address_line_2: Optional[str] = Field(None, description="The second line of the address, for example, a suite or apartment number")
    admin_area_2: Optional[str] = Field(None, description="A city, town, or village. Smaller than `admin_area_level_1`")
    admin_area_1: Optional[str] = Field(None, description="The highest-level sub-division in a country, which is usually a province, state, or ISO-3166-2 subdivision")
    postal_code: Optional[str] = Field(None, description="The postal code, which is the ZIP code or equivalent. Typically required for countries with a postal code or an equivalent")
    country_code: Optional[str] = Field(None, description="The 2-character ISO 3166-1 code that identifies the country or region. Note: The country code for Great Britain is `GB` and not `UK` as used in the top-level domain names for that country")


class CreateOrderParameters(BaseModel):
    """Parameters for creating an order."""
    currencyCode: CurrencyCode = Field(..., description="Currency code of the amount")
    items: List[OrderItem] = Field(..., description="The items in the order", max_items=50)
    discount: Optional[float] = Field(0, description="The discount amount for the order")
    shippingCost: Optional[float] = Field(0, description="The cost of shipping for the order")
    shippingAddress: Optional[ShippingAddressOrder] = Field(None, description="The shipping address for the order")
    notes: Optional[str] = Field(None, description="Notes for the order")
    returnUrl: Optional[str] = Field("https://example.com/returnUrl", description="The return URL after the order is created")
    cancelUrl: Optional[str] = Field("https://example.com/cancelUrl", description="The cancel URL if the user cancels the order")


class GetOrderParameters(BaseModel):
    """Parameters for retrieving an order."""
    id: str = Field(..., description="The order ID generated during create call")


class CaptureOrderParameters(BaseModel):
    """Parameters for capturing an order."""
    id: str = Field(..., description="The order ID generated during create call")


# === DISPUTE PARAMETERS ===

class DisputeState(str, Enum):
    """Dispute state enumeration."""
    REQUIRED_ACTION = "REQUIRED_ACTION"
    REQUIRED_OTHER_PARTY_ACTION = "REQUIRED_OTHER_PARTY_ACTION"
    UNDER_PAYPAL_REVIEW = "UNDER_PAYPAL_REVIEW"
    RESOLVED = "RESOLVED"
    OPEN_INQUIRIES = "OPEN_INQUIRIES"
    APPEALABLE = "APPEALABLE"


class ListDisputesParameters(BaseModel):
    """Parameters for listing disputes."""
    disputed_transaction_id: Optional[str] = Field(None, description="The transaction ID for which to list disputes")
    dispute_state: Optional[DisputeState] = Field(None, description="The state of the disputes to list")
    page_size: Optional[int] = Field(10, description="The number of records to return per page")
    page: Optional[int] = Field(1, description="The page number of the result set to fetch")


class GetDisputeParameters(BaseModel):
    """Parameters for retrieving a dispute."""
    dispute_id: str = Field(..., description="The ID of the dispute to retrieve")


class AcceptDisputeClaimParameters(BaseModel):
    """Parameters for accepting a dispute claim."""
    dispute_id: str = Field(..., description="The ID of the dispute to accept the claim for")
    note: str = Field(..., description="A note about why the seller is accepting the claim")


# === TRANSACTION PARAMETERS ===

class TransactionStatus(str, Enum):
    """Transaction status enumeration."""
    D = "D"  # Denied
    P = "P"  # Pending
    S = "S"  # Success
    V = "V"  # Voided


class ListTransactionsParameters(BaseModel):
    """Parameters for listing transactions."""
    transaction_id: Optional[str] = Field(None, description="The ID of the transaction to retrieve")
    transaction_status: Optional[TransactionStatus] = Field(None, description="The status of the transactions to list")
    start_date: Optional[str] = Field(None, description="Filters the transactions in the response by a start date and time, in Internet date and time format. Seconds are required. Fractional seconds are optional.")
    end_date: Optional[str] = Field(None, description="Filters the transactions in the response by an end date and time, in Internet date and time format. Seconds are required. Fractional seconds are optional. The maximum supported range is 31 days.")
    page_size: Optional[int] = Field(100, description="The number of records to return per page")
    page: Optional[int] = Field(1, description="The page number of the result set to fetch")
