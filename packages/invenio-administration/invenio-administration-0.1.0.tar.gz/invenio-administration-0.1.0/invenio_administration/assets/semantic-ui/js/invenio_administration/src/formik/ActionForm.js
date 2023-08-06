import React, { Component } from "react";
import PropTypes from "prop-types";
import { Form, Formik } from "formik";
import { InvenioAdministrationActionsApi } from "../api/actions";
import { Button, Modal } from "semantic-ui-react";
import { Form as SemanticForm } from "semantic-ui-react";
import _get from "lodash/get";
import { ErrorMessage } from "../ui_messages/messages";
import isEmpty from "lodash/isEmpty";
import { GenerateForm } from "./GenerateForm";

export class ActionForm extends Component {
  constructor(props) {
    super(props);
    const { resource } = props;

    this.state = {
      loading: false,
      error: undefined,
      formData: resource,
    };
  }

  onSubmit = async ({ formData }, e) => {
    this.setState({ loading: true });
    const { actionKey, actionSuccessCallback } = this.props;
    const actionEndpoint = this.getEndpoint(actionKey);

    try {
      const response = await InvenioAdministrationActionsApi.resourceAction(
        actionEndpoint,
        formData
      );
      this.setState({ loading: false });
      actionSuccessCallback(response.data);
    } catch (e) {
      console.error(e);
      this.setState({
        error: { header: "Action error", content: e, id: e.code },
      });
    }
  };

  onCancel = () => {
    const { resource, actionCancelCallback } = this.props;
    this.setState({ formData: resource });
    actionCancelCallback();
  };

  getEndpoint = (actionKey) => {
    const { resource } = this.props;
    let endpoint;
    // get the action endpoint from the current resource links
    endpoint = _get(resource.links.actions[actionKey]);

    // endpoint can be also within links, not links.action
    // TODO: handle it in a nicer way
    if (!endpoint) {
      endpoint = _get(resource.links[actionKey]);
    }
    if (!endpoint) {
      console.error("Action endpoint not found in the resource!");
    }
    return endpoint;
  };

  render() {
    const { actionSchema } = this.props;
    const { loading, formData, error } = this.state;
    return (
      <Formik initialValues={formData} onSubmit={this.onSubmit}>
        {(props) => (
          <SemanticForm as={Form} onSubmit={props.handleSubmit}>
            <GenerateForm jsonSchema={actionSchema} />
            {!isEmpty(error) && <ErrorMessage {...error} />}
            <Modal.Actions>
              <Button type="button" onClick={this.onCancel}>
                Cancel
              </Button>
              <Button type="submit" primary loading={loading}>
                Save
              </Button>
            </Modal.Actions>
          </SemanticForm>
        )}
      </Formik>
    );
  }
}

ActionForm.propTypes = {
  resource: PropTypes.object.isRequired,
  actionSchema: PropTypes.object.isRequired,
  actionKey: PropTypes.string.isRequired,
  actionSuccessCallback: PropTypes.func.isRequired,
  actionCancelCallback: PropTypes.func.isRequired,
};
