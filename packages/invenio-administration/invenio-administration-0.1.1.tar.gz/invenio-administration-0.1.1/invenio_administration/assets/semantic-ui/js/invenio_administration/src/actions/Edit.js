import React, { Component } from "react";
import { i18next } from "@translations/invenio_administration/i18next";
import { Button } from "semantic-ui-react";

export class Edit extends Component {
  render() {
    return (
      <Button
        icon="edit"
        labelPosition="left"
        content={i18next.t("Edit")}
        {...this.props}
      />
    );
  }
}
