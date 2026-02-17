#!/usr/bin/env python3
"""
OpenAPI 3.0 Specification Validator

Validates OpenAPI specs for correctness, completeness, and best practices.
"""

import json
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple


def load_spec(file_path: str) -> Tuple[Dict, List[str]]:
    """Load OpenAPI spec from YAML or JSON file."""
    errors = []
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith('.json'):
                spec = json.load(f)
            else:
                spec = yaml.safe_load(f)
        return spec, errors
    except Exception as e:
        errors.append(f"Failed to load spec: {str(e)}")
        return {}, errors


def validate_structure(spec: Dict) -> List[str]:
    """Validate basic OpenAPI structure."""
    errors = []

    # Check required top-level fields
    if 'openapi' not in spec:
        errors.append("Missing required field: 'openapi'")
    elif not spec['openapi'].startswith('3.0'):
        errors.append(f"Unsupported OpenAPI version: {spec['openapi']}")

    if 'info' not in spec:
        errors.append("Missing required field: 'info'")
    else:
        info = spec['info']
        if 'title' not in info:
            errors.append("Missing required field: 'info.title'")
        if 'version' not in info:
            errors.append("Missing required field: 'info.version'")

    if 'paths' not in spec:
        errors.append("Missing required field: 'paths'")
    elif not spec['paths']:
        errors.append("'paths' object is empty - at least one path is required")

    return errors


def validate_paths(spec: Dict) -> List[str]:
    """Validate path definitions."""
    errors = []
    warnings = []

    paths = spec.get('paths', {})
    for path, path_item in paths.items():
        # Check path format
        if not path.startswith('/'):
            errors.append(f"Path '{path}' must start with '/'")

        # Check for operations
        operations = ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']
        has_operation = any(op in path_item for op in operations)
        if not has_operation:
            warnings.append(f"Path '{path}' has no operations defined")

        # Validate each operation
        for method in operations:
            if method in path_item:
                operation = path_item[method]

                # Check for responses
                if 'responses' not in operation:
                    errors.append(f"{method.upper()} {path}: Missing 'responses'")
                elif not operation['responses']:
                    errors.append(f"{method.upper()} {path}: 'responses' is empty")

                # Check for summary or description
                if 'summary' not in operation and 'description' not in operation:
                    warnings.append(f"{method.upper()} {path}: Missing 'summary' or 'description'")

                # Check for operationId
                if 'operationId' not in operation:
                    warnings.append(f"{method.upper()} {path}: Missing 'operationId' (recommended)")

    return errors + warnings


def validate_schemas(spec: Dict) -> List[str]:
    """Validate component schemas."""
    errors = []
    warnings = []

    components = spec.get('components', {})
    schemas = components.get('schemas', {})

    for schema_name, schema in schemas.items():
        # Check for type
        if 'type' not in schema and '$ref' not in schema and 'allOf' not in schema and 'oneOf' not in schema and 'anyOf' not in schema:
            warnings.append(f"Schema '{schema_name}': Missing 'type' property")

        # Check for description
        if 'description' not in schema:
            warnings.append(f"Schema '{schema_name}': Missing 'description' (recommended)")

        # If object type, check for properties
        if schema.get('type') == 'object':
            if 'properties' not in schema:
                warnings.append(f"Schema '{schema_name}': Object type but no 'properties' defined")

    return errors + warnings


def validate_security(spec: Dict) -> List[str]:
    """Validate security definitions."""
    errors = []
    warnings = []

    components = spec.get('components', {})
    security_schemes = components.get('securitySchemes', {})

    # Check if security schemes are defined
    if not security_schemes:
        warnings.append("No security schemes defined (consider adding authentication)")

    # Validate each security scheme
    for scheme_name, scheme in security_schemes.items():
        if 'type' not in scheme:
            errors.append(f"Security scheme '{scheme_name}': Missing 'type'")

        scheme_type = scheme.get('type')
        if scheme_type == 'http':
            if 'scheme' not in scheme:
                errors.append(f"Security scheme '{scheme_name}': HTTP type requires 'scheme'")
        elif scheme_type == 'apiKey':
            if 'name' not in scheme:
                errors.append(f"Security scheme '{scheme_name}': apiKey type requires 'name'")
            if 'in' not in scheme:
                errors.append(f"Security scheme '{scheme_name}': apiKey type requires 'in'")
        elif scheme_type == 'oauth2':
            if 'flows' not in scheme:
                errors.append(f"Security scheme '{scheme_name}': oauth2 type requires 'flows'")

    return errors + warnings


def validate_examples(spec: Dict) -> List[str]:
    """Check for examples in request/response bodies."""
    warnings = []

    paths = spec.get('paths', {})
    for path, path_item in paths.items():
        operations = ['get', 'post', 'put', 'patch', 'delete']
        for method in operations:
            if method in path_item:
                operation = path_item[method]

                # Check request body examples
                if 'requestBody' in operation:
                    request_body = operation['requestBody']
                    content = request_body.get('content', {})
                    for media_type, media_type_obj in content.items():
                        if 'example' not in media_type_obj and 'examples' not in media_type_obj:
                            warnings.append(f"{method.upper()} {path}: Request body missing example")

                # Check response examples
                responses = operation.get('responses', {})
                for status_code, response in responses.items():
                    if status_code.startswith('2'):  # Success responses
                        content = response.get('content', {})
                        for media_type, media_type_obj in content.items():
                            if 'example' not in media_type_obj and 'examples' not in media_type_obj:
                                warnings.append(f"{method.upper()} {path}: Response {status_code} missing example")

    return warnings


def validate_best_practices(spec: Dict) -> List[str]:
    """Check for API design best practices."""
    warnings = []

    # Check for servers
    if 'servers' not in spec:
        warnings.append("No 'servers' defined (recommended to specify base URLs)")

    # Check for tags
    if 'tags' not in spec:
        warnings.append("No 'tags' defined (recommended for API organization)")

    # Check for contact info
    info = spec.get('info', {})
    if 'contact' not in info:
        warnings.append("No contact information in 'info' (recommended)")

    # Check for license
    if 'license' not in info:
        warnings.append("No license information in 'info' (consider adding)")

    # Check paths for REST conventions
    paths = spec.get('paths', {})
    for path in paths.keys():
        # Check for path parameters format
        if '{' in path and '}' in path:
            # Extract parameter names
            import re
            params = re.findall(r'\{([^}]+)\}', path)
            for param in params:
                if param.upper() == param or '_' in param:
                    warnings.append(f"Path '{path}': Parameter '{param}' should use camelCase")

        # Check for trailing slashes
        if path.endswith('/') and path != '/':
            warnings.append(f"Path '{path}': Avoid trailing slashes")

        # Check for verbs in path (anti-pattern)
        verbs = ['get', 'create', 'update', 'delete', 'fetch', 'list', 'add', 'remove']
        path_parts = path.lower().split('/')
        for verb in verbs:
            if verb in path_parts:
                warnings.append(f"Path '{path}': Avoid verbs in path (use HTTP methods instead)")

    return warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_openapi.py <spec-file.yaml>")
        sys.exit(1)

    spec_file = sys.argv[1]

    print(f"Validating OpenAPI specification: {spec_file}")
    print("=" * 60)

    # Load spec
    spec, load_errors = load_spec(spec_file)
    if load_errors:
        print("\n❌ LOAD ERRORS:")
        for error in load_errors:
            print(f"  - {error}")
        sys.exit(1)

    # Run validations
    all_errors = []
    all_warnings = []

    structure_errors = validate_structure(spec)
    all_errors.extend([e for e in structure_errors if 'Missing required' in e or 'Unsupported' in e])
    all_warnings.extend([e for e in structure_errors if e not in all_errors])

    path_issues = validate_paths(spec)
    all_errors.extend([e for e in path_issues if 'Missing' in e and 'required' in e.lower()])
    all_warnings.extend([e for e in path_issues if e not in all_errors])

    schema_issues = validate_schemas(spec)
    all_errors.extend([e for e in schema_issues if 'required' in e.lower()])
    all_warnings.extend([e for e in schema_issues if e not in all_errors])

    security_issues = validate_security(spec)
    all_errors.extend([e for e in security_issues if 'Missing' in e and 'requires' in e])
    all_warnings.extend([e for e in security_issues if e not in all_errors])

    example_warnings = validate_examples(spec)
    all_warnings.extend(example_warnings)

    best_practice_warnings = validate_best_practices(spec)
    all_warnings.extend(best_practice_warnings)

    # Report results
    if all_errors:
        print("\n❌ ERRORS:")
        for error in all_errors:
            print(f"  - {error}")

    if all_warnings:
        print("\n⚠️  WARNINGS:")
        for warning in all_warnings:
            print(f"  - {warning}")

    if not all_errors and not all_warnings:
        print("\n✅ Specification is valid with no issues!")
    elif not all_errors:
        print(f"\n✅ Specification is valid ({len(all_warnings)} warnings)")
    else:
        print(f"\n❌ Specification has {len(all_errors)} errors and {len(all_warnings)} warnings")
        sys.exit(1)


if __name__ == '__main__':
    main()
