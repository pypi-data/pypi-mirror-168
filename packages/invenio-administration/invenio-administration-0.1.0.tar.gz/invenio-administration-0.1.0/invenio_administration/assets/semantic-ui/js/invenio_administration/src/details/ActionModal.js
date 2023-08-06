// This file is part of InvenioAdministration
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import PropTypes from "prop-types";
import React, { Component } from "react";
import { i18next } from "@translations/invenio_administration/i18next";
import { Button, Modal, Header } from "semantic-ui-react";

class ActionModal extends Component {
  render() {
    const { action, trigger, children, modalOpen, toggleModal, actionTrigger } =
      this.props;

    return (
      <Modal role="dialog" open={modalOpen} trigger={trigger}>
        <Modal.Header>
          <Header as="h2">{i18next.t(action)}</Header>
        </Modal.Header>

        <Modal.Content>
          <Modal.Description>{children}</Modal.Description>
        </Modal.Content>

        <Modal.Actions>
          <Button
            onClick={toggleModal}
            floated="left"
            icon="cancel"
            labelPosition="left"
            content={i18next.t("Cancel")}
          />
          {actionTrigger}
        </Modal.Actions>
      </Modal>
    );
  }
}

export default ActionModal;

ActionModal.propTypes = {
  action: PropTypes.string.isRequired,
  children: PropTypes.object,
  modalOpen: PropTypes.bool,
  toggleModal: PropTypes.func.isRequired,
  trigger: PropTypes.object.isRequired,
  actionTrigger: PropTypes.object.isRequired,
};

ActionModal.defaultProps = {
  modalOpen: false,
  children: null,
};
