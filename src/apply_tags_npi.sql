-- Databricks notebook source
DECLARE OR REPLACE VARIABLE catalog_use STRING;

SET VAR catalog_use = :`bundle.catalog`; 
SELECT catalog_use;
