# Tiqets Supplier API Migration Guide from v1 to v2

As of November 1st, 2022, Tiqets has released a new version of
the [Tiqets Supplier API](https://tiqets.github.io/supplier-api/) which is both a simplification and an extension of the specification.

The changes in a nutshell:
* We've merged the concepts of full-day and timeslots
* We've added (limited) support for checkout questions
* We've added support for pricing

Questions? Contact us at: [apisupport@tiqets.com](mailto:apisupport@tiqets.com)

## Endpoints

All endpoints of version 2 are prepended with `/v2` instead of `/v1`

For example, to retrieve your product  catalog Tiqets would perform an `HTTP` request as follows:
```shell
GET https://your-api-domain/v2/products
```

The following table lists the required changes to migrate all endpoints to version 2 of the specification. For a complete list of the endpoints please refer to the official [Tiqets Supplier API Specification](https://tiqets.github.io/supplier-api/).

| Endpoint's Name      | HTTP Method | Endpoint's URL in v1 | Endpoint's URL in v2 |
| ----------- | ----------- | ----------- | ----------- |
| **Product Catalog**      | `GET`       | `/v1/products` | `/v2/products` |
| **Availability (variants)**   | `GET`        | `/v1/products/{product_id}/variants` | `/v2/products/{product_id}/availability` |
| **Availability (timeslots)**  | `GET`        | `/v1/products/{product_id}/timeslots` | `/v2/products/{product_id}/availability` |
| **Reservation**   | `POST`        | `/v1/products/{product_id}/reservation` | `/v2/products/{product_id}/reservation` |
| **Booking**   | `POST`        | `/v1/booking` | `/v2/booking` |
| **Cancellation**   | `DELETE`        | `/v1/booking` | `/v2/booking` |

### Product Catalog

The product catalog endpoint **MUST** be implemented by a v2-complaint API implementation. 

For details and examples please refer to the official [Product Endpoint Documentation](https://tiqets.github.io/supplier-api/#tag/Product-Catalog/operation/getProducts).

#### Changes Affecting the Endpoint's Requests

| Query Parameter       | Type of Change | v1          | v2          |
| ----------- | -----------    | ----------- | ----------- |
| `use_timeslots` | removed    | optional    | deleted     |

#### Changes Affecting the Endpoint's Response

| Field       | Type of Change | v1          | v2          | Description |
| ----------- | -----------    | ----------- | ----------- | ----------- |
| `max_tickets_per_order` | added    | N/A | optional | Specify the maximum amount of tickets that can be added to a single order. The absence of this field will mean that the product doesn't have such limits |
| `required_visitor_data` | added    | N/A | optional | A list of additional data that is required from each visitor (_full name_, _email_, _phone_, _address_, _passport id_, _date of birth_) |
| `required_order_data`   | added    | N/A | optional | A list of the additional fields required to be delivered on the order level (eg. _pickup location_, _nationality_, _zip code_) |

### Availability

For details and examples please refer to the official [Availability Endpoint Documentation](https://tiqets.github.io/supplier-api/#tag/Availability/operation/getAvailability).

V2 offers a *single* endpoint for disclosure of availability of products with or without timeslots.
Note that it's still not allowed for products to mix timeslots and full-day.

**In v1**
Availability fetching for products *with* timeslots:
```shell
GET https://your-api-domain/v1/products/{product-id}/timeslots
```
Availability fetching for products *without* timeslots (full-day):
```shell
GET https://your-api-domain/v1/products/{product-id}/variants
```
**In v2**
Availability fetching for products *with or without* timeslots:
```shell
GET https://your-api-domain/v2/products/{product-id}/availability
```

#### Changes Affecting the Endpoint's Response
**New Response Schema**

The schema of the availability endpoint's response has changed. The availability's response is a `JSON`
object. Each key defines an available day/timeslot, and it's specified using the format `YYYY-MM-DDTHH:MM`.

An example of a valid response is:

```json
{
  "2022-12-19T16:30": {
    "available_tickets": 100,
    "variants": [
      {
        "id": "TcGz7ywywiWYURHEWD",
        "name": "Adult",
        "available_tickets": 100,
        "price": {
          "amount": "10",
          "currency": "EUR"
        }
      },
      {
        "id": "hKl5sDxP9ont4GB",
        "name": "Child",
        "available_tickets": 10
      }
    ]
  }
}
```

This indicates that the product has 2 available variants on "2022-12-19" at "16:30". For additional details please refer to the official documentation of the endpoint.

If a product does not support timeslots then each 1st-level key in the `JSON` object **MUST** specify the time as
`T00:00`.

For example, the following is a valid availability response for a product that does not support timeslots:

```json
{
  "2022-12-19T00:00": {
    "available_tickets": 100,
    "variants": [
      {
        "id": "Y0J7aP1f3",
        "name": "Adult",
        "available_tickets": 100,
        "price": {
          "amount": "10",
          "currency": "EUR"
        }
      },
      {
        "id": "3cSQ8i",
        "name": "Child",
        "available_tickets": 10
      }
    ]
  }
}
```

**New `price` Field to Describe Variants**

The schema of the response's `variants` field includes a new, _optional_ field called `price`. The supplier may use this field to specify the price of an available variant.

> **Important Note** The presence of pricing doesn't imply that Tiqets shall ingest that price information. Only if the requirements for price ingestion are met then price ingestion *may* be enabled for certain products. Criteria currently are the type of agreement between the supplier and Tiqets and whether all variants carry the same commission percentage.

The schema of the `price` field is as follows:

```json
{
  "amount": string,
  "currency": string
}
```

For example, a valid value for the `variants` field could be:

```json
{
  "variants": [
      {
        "id": "1",
        "name": "Adult",
        "available_tickets": 100,
        "price": {
          "amount": "10.99",
          "currency": "EUR"
        }
      }
   ]
}
```

### Reservation

For details and examples please refer to the official [Reservation Endpoint Documentation](https://tiqets.github.io/supplier-api/#tag/Availability/operation/getAvailability).

#### Changes Affecting the Endpoint's Requests

| Field          | Type of Change | v1             | v2           |
| -----------    | -----------    | -----------    | -----------  |
| `datetime`     | added          |  N/A           |  required    |
| `timeslot_id`  | removed        |  `timeslot_id` |  N/A         |
| `date`         | removed        |  `date`        |  N/A         |
| `required_order_data`         | added        |  N/A        |  `required_order_data`        |
| `required_visitor_data`         | added        |  N/A        |  `required_visitor_data`     |

#### Changes Affecting the Endpoint's Response

| Field          | Type of Change | v1             | v2           |
| -----------    | -----------    | -----------    | -----------  |
| `pricing`      | added          |  N/A           |  optional    |

If a product provides pricing information, ie. the product's attribute `provides_pricing=true`, then the response to a 
reservation request for that product MUST include the attribute `pricing` with prices for all the variants in the 
reservation. 

### Booking

For details and examples please refer to the official [Booking Endpoint Documentation](https://tiqets.github.io/supplier-api/#tag/Booking/operation/booking).

#### Changes Affecting the Endpoint's Requests

V2 supports an optional `HTTP` header named `TIQETS-TEST-ORDER`. This header is used by the integration test tool to make a booking request and give you the opportunity to mark the booking as a **test booking**.

**Important**: Your implementation **MUST** respond with a valid `HTTP` response and **MUST** mark the booking as a **test booking** in their internal systems.

#### Changes Affecting the Endpoint's Response

| Field       | Type of Change | v1          | v2          |
| ----------- | -----------    | ----------- | ----------- |
| `barcode_position` | renamed    | `barcode_position`    | `barcode_scope`     |


## Errors

In API v2 some error codes have been deprecated. Make sure to update your implementation accordingly.

| Endpoint         | Error Code   | v1          | v2          |
| -----------      | -----------  | ----------- | ----------- |
| `/v2/products/{product_id}/availability` | `2009`       | present     | removed     |
| `/v2/products/{product_id}/reservation`  | `2006`       | present     | removed     |
| `/v2/products/{product_id}/reservation`  | `2010`       | present     | removed     |
| `/v2/products/{product_id}/reservation`  | `1003`       | N/A         | new         |
| `/v2/booking/{booking_id}`      | `3005`       | N/A         | new         |

Please refer to the [Official API Documentation](https://tiqets.github.io/supplier-api/) for a full list of the error codes supported in v2.