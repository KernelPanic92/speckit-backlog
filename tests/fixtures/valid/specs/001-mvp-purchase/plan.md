# Implementation Plan: First online purchase

## Project Structure

The purchase service lives in `app/`; executable Gherkin scenarios live in `tests/acceptance/`.

## Contracts

Catalog queries return current names and store-currency prices. Payment authorization is idempotent.
