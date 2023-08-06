# What it does
This package takes NoSQL data as input and transforms it into flattened SQL-like data. It can be useful in many cases. For example, imagine you have an application that uses `mongo` as the database but your data warehouse is `Google BigQuery` which is based on RDBMS, so basically SQL. In this case, you will have to flatten your data so you can push them to `BigQuery` tables.

# Installation
Use `pip install flatten-nosql` to install the package. You will need `pandas` installed on your machine since this library depends on it.

# NoSQL to SQL conversion

Check `driver-flattening` notebook inside `flattener` directory for an example usage.

## Warning
 * If your data has nested arrays inside nested arrays, make sure you specify depth. By default, the module will go as deep as possible. 
 * In some cases, memory requirement may be extremely high due to the nature of flattening. Note that, when we flatten a certain denormalized data, it can have a lot of redundant data in it, specially, if you did not normalize and denormalize your database design before development. A normalized and denormalized NoSQL database is not the same as a default NoSQL database which has denormalized looking data in it. Even if you use NoSQL as your preferred data storing format, you should always normalize your database like you would in a SQL database and then denormalize again if necessary. Otherwise, if you attempt flattening the complete data, it is possible that you will face memory issues. Flattening process can be insanely memory hungry if database was not properly designed.
 * The definition of `depth` in this package is based on whether a certain field has an array of dictionary or not. Check the example in the driver notebook. 
