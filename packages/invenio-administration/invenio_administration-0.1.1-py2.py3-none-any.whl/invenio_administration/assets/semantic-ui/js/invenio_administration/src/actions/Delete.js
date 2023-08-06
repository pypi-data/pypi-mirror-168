import React, { Component } from "react";
import PropTypes from "prop-types";
import { i18next } from "@translations/invenio_administration/i18next";
import { Button, Icon } from "semantic-ui-react";
import { InvenioAdministrationActionsApi } from "../api/actions";
import { NotificationContext } from "../ui_messages/context";

export class Delete extends Component {
  constructor(props) {
    super(props);
    this.state = { loading: false };
  }

  static contextType = NotificationContext;

  handleOnButtonClick = async () => {
    const { successCallback, resource, apiEndpoint, idKeyPath } = this.props;
    const { addNotification } = this.context;
    try {
      await InvenioAdministrationActionsApi.deleteResource(
        resource,
        apiEndpoint,
        idKeyPath
      );
      successCallback();
    } catch (e) {
      console.error(e);
      addNotification({
        title: i18next.t(`Unexpected exception: ${e.response.code}`),
        content: i18next.t(
          `The resource could not be deleted. Error: ${e.response.data}`
        ),
      });
    }
  };

  render() {
    const { loading } = this.state;
    return (
      <Button
        labelPosition="left"
        icon
        negative
        onClick={this.handleOnButtonClick}
        loading={loading}
      >
        <Icon name="trash alternate" />
        {i18next.t("Delete")}
      </Button>
    );
  }
}

Delete.propTypes = {
  apiEndpoint: PropTypes.string.isRequired,
  resource: PropTypes.object.isRequired,
  successCallback: PropTypes.func.isRequired,
  idKeyPath: PropTypes.string.isRequired,
};
