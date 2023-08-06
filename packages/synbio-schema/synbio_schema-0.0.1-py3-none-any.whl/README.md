# synbio-schema

A schema for synthetic biology, inspired by IARPA FELIX

## Website

* [https://semantic-synbio.github.io/synbio-schema](https://semantic-synbio.github.io/synbio-schema)

## Repository Structure

* [examples/](examples/) - example data
* [project/](project/) - project files (do not edit these)
* [src/](src/) - source files (edit these)
    * [synbio_schema](src/synbio_schema)
        * [schema](src/synbio_schema/schema) -- LinkML schema (edit this)
* [datamodel](src/synbio_schema/datamodel) -- Generated python datamodel
* [tests](tests/) - python tests

## Developer Documentation

<details>
Use the `make` command to generate project artefacts:

- `make all`: make everything
- `make deploy`: deploys site

</details>

## Credits

this project was made with [linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter)
