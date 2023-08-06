import React, { Component } from "react";
import PropTypes from "prop-types";
import { Form, Formik } from "formik";
import { Form as SemanticForm } from "semantic-ui-react";
import { InvenioAdministrationActionsApi } from "../api/actions";
import { Button } from "semantic-ui-react";
import { NotificationContext } from "../ui_messages/context";
import { ErrorMessage } from "../ui_messages/messages";
import _isEmpty from "lodash/isEmpty";
import { GenerateForm } from "./GenerateForm";

export class AdminForm extends Component {
  constructor(props) {
    super(props);
    const { resource } = props;

    this.state = {
      error: undefined,
      formData: resource ? resource : {},
    };
  }

  static contextType = NotificationContext;

  onSubmit = async (values, actions) => {
    const { apiEndpoint, pid, successCallback, create } = this.props;
    const { addNotification } = this.context;
    let response;
    try {
      if (create) {
        response = await InvenioAdministrationActionsApi.createResource(
          apiEndpoint,
          values
        );
      } else {
        response = await InvenioAdministrationActionsApi.editResource(
          apiEndpoint,
          pid,
          values
        );
      }
      actions.setSubmitting(false);
      actions.resetForm({ values: { ...values } });
      addNotification({
        title: "Success",
        content: "Your changes were successfully submitted",
        type: "success",
      });
      successCallback(response.data);
    } catch (e) {
      console.error(e);
      this.setState({
        error: { header: "Form error", content: e, id: e.code },
      });
    }
  };

  onCancel = () => {
    const { resource } = this.props;
    this.setState({ formData: resource });
  };

  render() {
    const { resourceSchema, create, formFields } = this.props;
    const { formData, error } = this.state;

    return (
      <Formik initialValues={formData} onSubmit={this.onSubmit}>
        {(props) => (
          <SemanticForm
            as={Form}
            onSubmit={(e) => {
              e.preventDefault();
              props.handleSubmit();
            }}
          >
            <GenerateForm
              formFields={formFields}
              jsonSchema={resourceSchema}
              create={create}
            />
            {!_isEmpty(error) && <ErrorMessage {...error} />}
            <Button
              type="button"
              onClick={this.onCancel}
              loading={props.isSubmitting}
              disabled={props.isSubmitting}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              primary
              loading={props.isSubmitting}
              disabled={props.isSubmitting}
            >
              Save
            </Button>
          </SemanticForm>
        )}
      </Formik>
    );
  }
}

AdminForm.propTypes = {
  resource: PropTypes.object,
  resourceSchema: PropTypes.object.isRequired,
  apiEndpoint: PropTypes.string.isRequired,
  pid: PropTypes.string,
  create: PropTypes.bool,
  formFields: PropTypes.object,
  successCallback: PropTypes.func,
};

AdminForm.defaultProps = {
  resource: undefined,
  create: false,
  pid: undefined,
  formFields: undefined,
  successCallback: () => {},
};
