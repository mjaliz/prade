# Django ORM

## Model.objects ---> will return the Manager

## Model.objects.all() ---> query set

### Query set will be called in some scenarios

- iterating overt the query set:
  - for product in query_set
- converting query set to list:
  - list(query_set)
- slicing query set:
  - query_set[:5]

## Model.objects.count() ---> the number of model in database not query set

## Model.objects.get(pk=1) ---> return object with primary key = 1

- we should handle exception for this with ObjectDoseNotExist exception
- if we don't want to handle exception we should use Model.objects.filter(pk=0).first() and this will return None if object dose not exits.

## Model.objects.filter(pk=0).exists() ---> return a boolean

# Filtering objects

## Product.objects.filter(unit_price=20) ---> return products with unit_price equal to 20

## Product.objects.filter(unit_price\_\_gt=20) ---> return products with unit_price greater than 20

# Check for all field lookups ---> search django query set api -> field lookups

## Product.objects.filter(unit_price\_\_range=(20, 30)) ---> return the product with uint_price between 20 and 30

## Product.objects.filter(collection\_\_id=1) ---> return the products in Collection class with id=1

## Product.objects.filter(collection\_\_id\_\_gt=1) ---> return the products in Collection class with id greater than 1

## Product.objects.filter(collection\_\_id\_\_range=(1,2,3)) ---> return all the products in any of 1,2,3

## Product.objects.filter(title\_\_contains='coffee') ---> return all products that contains coffee in their title -> \_\_contains is case sensitive for insensitive use -> \_\_icontains

## Product.objects.filter(last_update\_\_year=2021) ---> return all products that the year of their last_update is equal to 2021 -> we can also use \_\_date or \_\_day , ...

## Product.objects.filter(description\_\_isnull=True) ---> return all products with null description
