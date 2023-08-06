import React, { Component } from "react";
import PropTypes from "prop-types";
import isEmpty from "lodash/isEmpty";
import { ResourceActions } from "./ResourceActions";
import { ActionsDropdown } from "./ActionsDropdown";
import { Button, Icon } from "semantic-ui-react";
import { AdminUIRoutes } from "../routes";
import { DeleteModalTrigger } from "./DeleteModalTrigger";

export class Actions extends Component {
  render() {
    const {
      title,
      resourceName,
      displayEdit,
      displayDelete,
      actions,
      apiEndpoint,
      resource,
      successCallback,
      idKeyPath,
      listUIEndpoint,
      disableDelete,
      disableEdit,
    } = this.props;

    // if number of actions is greater than 3, we display all in a dropdown
    const displayAsDropdown =
      displayEdit && displayDelete && Object.keys(actions).length > 1;

    if (displayAsDropdown) {
      return (
        <ActionsDropdown
          title={title}
          resourceName={resourceName}
          apiEndpoint={apiEndpoint}
          resource={resource}
          successCallback={successCallback}
          idKeyPath={idKeyPath}
          actions={actions}
          displayEdit={displayEdit}
          displayDelete={displayDelete}
        />
      );
    } else {
      return (
        <Button.Group size="tiny" className="relaxed">
          {!isEmpty(actions) && (
            <ResourceActions
              resource={resource}
              successCallback={successCallback}
              idKeyPath={idKeyPath}
              actions={actions}
              apiEndpoint={apiEndpoint}
            />
          )}
          {displayEdit && (
            <Button
              as="a"
              disabled={disableEdit}
              href={AdminUIRoutes.editView(listUIEndpoint, resource, idKeyPath)}
              icon
              labelPosition="left"
            >
              <Icon name="pencil" />
              Edit
            </Button>
          )}
          {displayDelete && (
            <DeleteModalTrigger
              title={title}
              resourceName={resourceName}
              apiEndpoint={apiEndpoint}
              resource={resource}
              successCallback={successCallback}
              idKeyPath={idKeyPath}
              disabled={disableDelete}
            />
          )}
        </Button.Group>
      );
    }
  }
}

Actions.propTypes = {
  title: PropTypes.string.isRequired,
  resourceName: PropTypes.string.isRequired,
  displayEdit: PropTypes.bool,
  displayDelete: PropTypes.bool,
  disableDelete: PropTypes.bool,
  disableEdit: PropTypes.bool,
  apiEndpoint: PropTypes.string,
  resource: PropTypes.object.isRequired,
  successCallback: PropTypes.func.isRequired,
  idKeyPath: PropTypes.string,
  actions: PropTypes.object.isRequired,
  listUIEndpoint: PropTypes.string.isRequired,
};

Actions.defaultProps = {
  displayEdit: true,
  displayDelete: true,
  disableDelete: false,
  disableEdit: false,
  apiEndpoint: undefined,
  idKeyPath: "pid",
};
