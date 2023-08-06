import React, { Component } from "react";
import PropTypes from "prop-types";
import { Dropdown, Button } from "semantic-ui-react";
import { ResourceActions } from "./ResourceActions";
import isEmpty from "lodash/isEmpty";
import { i18next } from "@translations/invenio_administration/i18next";
import { DeleteModalTrigger } from "./DeleteModalTrigger";

export class ActionsDropdown extends Component {
  render() {
    const {
      title,
      resourceName,
      displayEdit,
      displayDelete,
      apiEndpoint,
      resource,
      successCallback,
      idKeyPath,
      actions,
    } = this.props;
    return (
      <Dropdown>
        {!isEmpty(actions) && (
          <ResourceActions
            resource={resource}
            successCallback={successCallback}
            idKeyPath={idKeyPath}
            actions={actions}
            apiEndpoint={apiEndpoint}
            Element={Dropdown.Item}
            trigger={
              <Button
                icon="cog"
                size="tiny"
                className="transparent rel-ml-1"
                aria-label={i18next.t("Open list of actions")}
              />
            }
          />
        )}
        {displayEdit && <Dropdown.Item>Edit</Dropdown.Item>}
        {displayDelete && (
          <DeleteModalTrigger
            title={title}
            resourceName={resourceName}
            apiEndpoint={apiEndpoint}
            resource={resource}
            successCallback={successCallback}
            idKeyPath={idKeyPath}
            Element={Dropdown.Item}
          />
        )}
      </Dropdown>
    );
  }
}

ActionsDropdown.propTypes = {
  title: PropTypes.string.isRequired,
  resourceName: PropTypes.string.isRequired,
  displayEdit: PropTypes.bool,
  displayDelete: PropTypes.bool,
  apiEndpoint: PropTypes.string.isRequired,
  resource: PropTypes.object.isRequired,
  successCallback: PropTypes.func.isRequired,
  idKeyPath: PropTypes.string.isRequired,
  actions: PropTypes.object.isRequired,
};

ActionsDropdown.defaultProps = {
  displayDelete: true,
  displayEdit: true,
};
