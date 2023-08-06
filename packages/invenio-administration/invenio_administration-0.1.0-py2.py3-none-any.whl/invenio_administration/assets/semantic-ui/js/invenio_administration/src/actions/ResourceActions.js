import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button, Modal } from "semantic-ui-react";
import { ActionForm } from "../formik/ActionForm";

export class ResourceActions extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modalOpen: false,
      modalHeader: undefined,
      modalBody: undefined,
    };
  }

  onModalTriggerClick = (e, { payloadSchema, dataName, dataActionKey }) => {
    const { resource } = this.props;
    this.setState({
      modalOpen: true,
      modalHeader: dataName,
      modalBody: (
        <ActionForm
          actionKey={dataActionKey}
          actionSchema={payloadSchema}
          actionSuccessCallback={this.onModalClose}
          actionCancelCallback={this.onModalClose}
          resource={resource}
        />
      ),
    });
  };

  onModalClose = () => {
    const { successCallback } = this.props;
    this.setState({
      modalOpen: false,
      modalHeader: undefined,
      modalBody: undefined,
    });
    successCallback();
  };

  render() {
    const { actions, Element } = this.props;
    const { modalOpen, modalHeader, modalBody } = this.state;
    return (
      <>
        {Object.entries(actions).map(([actionKey, actionConfig]) => {
          return (
            <Element
              key={actionKey}
              onClick={this.onModalTriggerClick}
              payloadSchema={actionConfig.payload_schema}
              dataName={actionConfig.text}
              dataActionKey={actionKey}
            >
              {actionConfig.text}
            </Element>
          );
        })}
        <Modal open={modalOpen}>
          {modalHeader && <Modal.Header>{modalHeader}</Modal.Header>}
          {modalBody && <Modal.Content>{modalBody}</Modal.Content>}
        </Modal>
      </>
    );
  }
}

ResourceActions.propTypes = {
  resource: PropTypes.object.isRequired,
  successCallback: PropTypes.func.isRequired,
  actions: PropTypes.shape({
    text: PropTypes.string.isRequired,
    payload_schema: PropTypes.object.isRequired,
    order: PropTypes.number.isRequired,
  }),
  Element: PropTypes.node,
};

ResourceActions.defaultProps = {
  Element: Button,
  actions: undefined,
};
