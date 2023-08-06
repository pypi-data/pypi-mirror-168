import React from "react";
import ReactDOM from "react-dom";
import { EditPage } from "./EditPage";
import _get from "lodash/get";
import { NotificationController } from "../ui_messages/context";

const domContainer = document.getElementById("invenio-administration-edit-root");
const resourceSchema = JSON.parse(domContainer.dataset.resourceSchema);
const apiEndpoint = _get(domContainer.dataset, "apiEndpoint");
const pid = JSON.parse(domContainer.dataset.pid);
const formFields = JSON.parse(domContainer.dataset.formFields);
const listUIEndpoint = domContainer.dataset.listEndpoint;

ReactDOM.render(
  <NotificationController>
    <EditPage
      resourceSchema={resourceSchema}
      apiEndpoint={apiEndpoint}
      formFields={formFields}
      pid={pid}
      listUIEndpoint={listUIEndpoint}
    />
  </NotificationController>,
  domContainer
);
