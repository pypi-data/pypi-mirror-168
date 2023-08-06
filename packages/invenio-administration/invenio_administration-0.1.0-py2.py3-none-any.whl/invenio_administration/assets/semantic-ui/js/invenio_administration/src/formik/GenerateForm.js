import React from "react";
import { Input, AutocompleteDropdown } from "react-invenio-forms";
import _capitalize from "lodash/capitalize";
import PropTypes from "prop-types";
import { Form, Segment, Header } from "semantic-ui-react";
import { AdminArrayField } from "./array";
import _isEmpty from "lodash/isEmpty";
import { sortFields } from "../components/utils";

const fieldsMap = {
  string: Input,
  integer: Input,
  uuid: Input,
  datetime: Input,
};

const generateFieldProps = (fieldName, fieldSchema, parentField, isCreate) => {
  let currentFieldName;

  const fieldLabel = fieldSchema.title
    ? _capitalize(fieldSchema.title)
    : _capitalize(fieldName);

  if (parentField) {
    currentFieldName = `${parentField}.${fieldName}`;
  } else {
    currentFieldName = fieldName;
  }

  return {
    fieldPath: currentFieldName,
    key: currentFieldName,
    label: fieldLabel,
    required: fieldSchema.required,
    disabled: fieldSchema.readOnly || (fieldSchema.createOnly && !isCreate),
  };
};

const mapFormFields = (obj, parentField, isCreate, formFields) => {
  if (!obj) {
    return null;
  }

  const sortedFields = sortFields(obj);

  const elements = Object.entries(sortedFields).map(([fieldName, fieldSchema]) => {
    const fieldProps = generateFieldProps(
      fieldName,
      fieldSchema,
      parentField,
      isCreate
    );

    const showField =
      _isEmpty(formFields) ||
      Object.prototype.hasOwnProperty.call(formFields, fieldProps.fieldPath);

    if (!showField) {
      return null;
    }

    if (fieldSchema.type === "array") {
      return (
        <AdminArrayField
          key={fieldProps.fieldPath}
          fieldSchema={fieldSchema}
          isCreate={isCreate}
          mapFormFields={mapFormFields}
          formFields={formFields}
          {...fieldProps}
        />
      );
    }

    if (fieldSchema.type === "vocabulary") {
      return (
        <AutocompleteDropdown
          key={fieldProps.fieldPath}
          required={fieldSchema.required}
          autocompleteFrom={`/api/vocabularies/${fieldSchema.metadata.type}`}
          {...fieldProps}
        />
      );
    }

    if (fieldSchema.type === "object") {
      // nested fields
      return (
        <React.Fragment key={fieldProps.fieldPath}>
          <Header attached="top" as="h5">
            {fieldProps.label}
          </Header>
          <Segment attached="bottom">
            <Form.Group grouped>
              {mapFormFields(
                fieldSchema.properties,
                fieldProps.fieldPath,
                isCreate,
                formFields
              )}
            </Form.Group>
          </Segment>
        </React.Fragment>
      );
    }

    const Element = fieldsMap[fieldSchema.type];
    return <Element {...fieldProps} key={fieldProps.fieldPath} />;
  });

  return elements;
};

export const GenerateForm = ({ jsonSchema, create, formFields }) => {
  const properties = jsonSchema;
  return <>{mapFormFields(properties, undefined, create, formFields)}</>;
};

GenerateForm.propTypes = {
  jsonSchema: PropTypes.object.isRequired,
  create: PropTypes.bool,
  formFields: PropTypes.object,
};

GenerateForm.defaultProps = {
  create: false,
  formFields: undefined,
};
