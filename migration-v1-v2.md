# Tiqets Supplier API Migration Guide from v1 to v2

Starting on November 1st, 2022, Tiqets has released a new version of 
the [Tiqets Supplier API](https://tiqets.github.io/supplier-api/). The new version of the API....

For questions related to this migration guide or about the API you can contact us at: 
[apisupport@tiqets.com](mailto:apisupport@tiqets.com)

## Endpoints

Migrating the API from version 1 to version 2 requires updating the endpoints' URLs to drop the v1 string and
replace it with v2.

For example, to retrieve the list of products Tiqets would make an `HTTP` request as follows:

```shell
GET https://your-api-domain/v2/products
```

The following table summarises the changes that are required to migrate all the endpoints to support v2 of the
specification. For a complete list of the endpoints please refer to the official
[Tiqets Supplier API Specification](https://tiqets.github.io/supplier-api/).

| Endpoint’s Name      | HTTP Method | Endpoint’s URL in v1 | Endpoint’s URL in v2 |
| ----------- | ----------- | ----------- | ----------- |
| **Product Catalog**      | `GET`       | `https://your-api-domain/v1/products` | `https://your-api-domain/v2/products` |
| **Availability**   | `GET`        | `https://your-api-domain/v1/products/{product_id}/variants` | `https://your-api-domain/v2/products/{product_id}/availability` |
| **Availability**  | `GET`        | `https://your-api-domain/v1/products/{product_id}/timeslots` | `https://your-api-domain/v2/products/{product_id}/availability` |
| **Reservation**   | `POST`        | `https://your-api-domain/v1/products/{product_id}/reservation` | `https://your-api-domain/v2/products/{product_id}/reservation` |
| **Booking**   | `POST`        | `https://your-api-domain/v1/booking` | `https://your-api-domain/v2/booking` |
| **Cancellation**   | `DELETE`        | `https://your-api-domain/v1/booking` | `https://your-api-domain/v2/booking` |

### Product Catalog

For details and examples please refer to the official 
[Product Endpoint Documentation](https://tiqets.github.io/supplier-api/#tag/Product-Catalog/operation/getProducts).

#### Changes Affecting the Endpoint's Response

| Field       | Type of Change | v1          | v2          | Description |
| ----------- | -----------    | ----------- | ----------- | ----------- |
| `max_tickets_per_order` | added    | N/A | optional | Specify the maximum amount of tickets that can be added to a single order. The absence of this field will mean that the product doesn't have such limits |
| `required_visitor_data` | added    | N/A | optional | a list of additional data that is required from each visitor (_full name_, _email_, _phone_, _address_, _passport id_, _date of birth_) |
| `required_order_data`   | added    | N/A | optional | a list of the additional fields required to be delivered on the order level (eg. _pickup location_, _nationality_, _zip code_) |

#### Changes Affecting the Endpoint's Requests

| Field       | Type of Change | v1          | v2          |
| ----------- | -----------    | ----------- | ----------- |
| `use_timeslots` | removed    | optional    | deleted     |

### Availability

For details and examples please refer to the official 
[Availability Endpoint Documentation](https://tiqets.github.io/supplier-api/#tag/Availability/operation/getAvailability).

The new API introduces a new endpoint that allows Tiqets to fetch the availability of a product. In v1, the client would 
make an `HTTP` request to 2 different endpoints depending on whether the product supports timeslots or not.

In v1, if a product supports timeslots then the client would request availability in the following manner:

```shell
GET https://your-api-domain/v1/products/{product-id}/timeslots
```

If, on the other hand the product doesn't support timeslots then the client would make the following request:

```shell
GET https://your-api-domain/v1/products/{product-id}/variants
```

In v2 of the API the endpoints above have been deprecated and replaced with a new endpoint. To retrieve availability of 
a product the client would make a request as follows:

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
        "id": "1",
        "name": "Adult",
        "available_tickets": 100,
        "price": {
          "face_value": "10",
          "currency": "EUR"
        }
      },
      {
        "id": "2",
        "name": "Child",
        "available_tickets": 10
      }
    ]
  }
}
```

This indicates that the product has 2 available variants on "2022-12-19" at "16:30". For additional details please refer 
to the official documentation of the endpoint.

If a product does not support timeslots then each 1st-level key in the `JSON` object must specify the time as 
`T00:00`. 

For example, the following is a valid availability response for a product that does not support timeslots:

```json
{
  "2022-12-19T00:00": {
    "available_tickets": 100,
    "variants": [
      {
        "id": "1",
        "name": "Adult",
        "available_tickets": 100,
        "price": {
          "face_value": "10",
          "currency": "EUR"
        }
      },
      {
        "id": "2",
        "name": "Child",
        "available_tickets": 10
      }
    ]
  }
}
```

**New `price` Field to Describe Variants**:

The schema of the response's `variants` field includes a new, _optional_ field called `price`. The supplier can use this 
field to specify the price of an available variant. The schema of the `price` field is as follows:

```json
{
  "face_value": string,
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
          "face_value": "10.99",
          "currency": "EUR"
        }
      }
   ]
}
```

### Reservation

For details and examples please refer to the official 
[Reservation Endpoint Documentation](https://tiqets.github.io/supplier-api/#tag/Availability/operation/getAvailability).

#### Changes Affecting the Endpoint's Requests

| Field          | Type of Change | v1             | v2           |
| -----------    | -----------    | -----------    | -----------  |
| `datetime`     | added          |  N/A           |  required    |
| `timeslot_id`  | removed        |  `timeslot_id` |  N/A         |
| `date`         | removed        |  `date`        |  N/A         |
| `required_order_data`         | added        |  N/A        |  `required_order_data`        |
| `required_visitor_data`         | added        |  N/A        |  `required_visitor_data`        |

The lists of possible values for these fields are:

- `required_order_data`: **PICKUP_LOCATION**, **DROPOFF_LOCATION**, **NATIONALITY**, **FLIGHT_NUMBER**, **PASSPORT_ID**
- `required_visitor_data`: **FULL_NAME**, **EMAIL**, **PHONE**, **ADDRESS**, **PASSPORT_ID**, **DATE_OF_BIRTH**

### Booking

For details and examples please refer to the official 
[Booking Endpoint Documentation](https://tiqets.github.io/supplier-api/#tag/Booking/operation/booking).

#### Changes Affecting the Endpoint's Response

| Field       | Type of Change | v1          | v2          |
| ----------- | -----------    | ----------- | ----------- |
| `barcode_position` | renamed    | `barcode_position`    | `barcode_scope`     |


#### Changes Affecting the Endpoint's Requests

The new version of the API supports an optional `HTTP` header named `TIQETS-TEST-ORDER`. Using this header the client 
can make a booking request and flag the booking as a **test booking**. 

**Important**: the API server **MUST** respond with a valid `HTTP` response and, **MUST** mark the booking as 
**test booking** in their internal systems.
 
## Errors

In API v2 some error codes have been deprecated. Make sure to update your API server accordingly.

| Endpoint         | Error Code   | v1          | v2          |
| -----------      | -----------  | ----------- | ----------- |
| **Availability** | `2009`       | present     | removed     |
| **Reservation**  | `2006`       | present     | removed     |
| **Reservation**  | `2010`       | present     | removed     |
| **Reservation**  | `1003`       | N/A         | new         |

Please refer to the [Official API Documentation](https://tiqets.github.io/supplier-api/) for a full list of the error 
codes supported in v2.