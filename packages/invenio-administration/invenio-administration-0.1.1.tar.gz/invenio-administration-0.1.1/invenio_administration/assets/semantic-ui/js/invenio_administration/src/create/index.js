import React from "react";
import ReactDOM from "react-dom";
import { CreatePage } from "./CreatePage";
import _get from "lodash/get";
import { NotificationController } from "../ui_messages/context";

const domContainer = document.getElementById("invenio-administration-create-root");
const resourceSchema = JSON.parse(domContainer.dataset.resourceSchema);
const apiEndpoint = _get(domContainer.dataset, "apiEndpoint");
const formFields = JSON.parse(domContainer.dataset.formFields);
const listUIEndpoint = domContainer.dataset.listEndpoint;

ReactDOM.render(
  <NotificationController>
    <CreatePage
      resourceSchema={resourceSchema}
      apiEndpoint={apiEndpoint}
      formFields={formFields}
      listUIEndpoint={listUIEndpoint}
    />
  </NotificationController>,
  domContainer
);
