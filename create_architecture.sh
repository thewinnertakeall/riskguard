#!/usr/bin/env bash

set -e

echo "========================================"
echo "RiskGuard - Arquitectura POO"
echo "========================================"

mkdir -p \
    domain/entities \
    domain/value_objects \
    domain/repositories \
    domain/services \
    application/use_cases \
    application/dto \
    infrastructure/database \
    infrastructure/repositories \
    infrastructure/rdf \
    infrastructure/sparql \
    app/routers

touch \
    domain/__init__.py \
    domain/entities/__init__.py \
    domain/value_objects/__init__.py \
    domain/repositories/__init__.py \
    domain/services/__init__.py \
    application/__init__.py \
    application/use_cases/__init__.py \
    application/dto/__init__.py \
    infrastructure/__init__.py \
    infrastructure/database/__init__.py \
    infrastructure/repositories/__init__.py \
    infrastructure/rdf/__init__.py \
    infrastructure/sparql/__init__.py \
    app/__init__.py \
    app/routers/__init__.py

echo
echo "=== ESTRUCTURA CREADA ==="

find domain application infrastructure app \
    -maxdepth 3 \
    -type f \
    | sort

echo
echo "========================================"
echo "OK"
echo "========================================"
