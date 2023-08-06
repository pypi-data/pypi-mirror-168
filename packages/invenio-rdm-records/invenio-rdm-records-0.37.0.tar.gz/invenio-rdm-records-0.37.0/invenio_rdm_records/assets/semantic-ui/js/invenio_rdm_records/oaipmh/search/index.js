// This file is part of InvenioRdmRecords
// Copyright (C) 2022 CERN.
//
// Invenio RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import defaultComponents from "@js/invenio_administration/src/search/search.js";
import { createSearchAppInit } from "@js/invenio_search_ui";
import { SearchResultItem } from "./SearchResultItem";
import { parametrize } from "react-overridable";
import _get from "lodash/get";
import { NotificationController } from "@js/invenio_administration/src/ui_messages/context";

const domContainer = document.getElementById("invenio-search-config");

const sortColumns = (columns) =>
  Object.entries(columns).sort((a, b) => a[1].order > b[1].order);
const title = JSON.parse(domContainer.dataset.title);
const resourceName = JSON.parse(domContainer.dataset.resourceName);
const columns = JSON.parse(domContainer.dataset.fields);
const sortedColumns = sortColumns(columns);
const displayEdit = JSON.parse(domContainer.dataset.displayEdit);
const displayDelete = JSON.parse(domContainer.dataset.displayDelete);
const displayRead = JSON.parse(domContainer.dataset.displayRead);
const actions = JSON.parse(domContainer.dataset.actions);
const apiEndpoint = _get(domContainer.dataset, "apiEndpoint");
const idKeyPath = JSON.parse(_get(domContainer.dataset, "pidPath", "pid"));
const listUIEndpoint = domContainer.dataset.listEndpoint;

const SearchResultItemWithConfig = parametrize(SearchResultItem, {
  title: title,
  resourceName: resourceName,
  columns: sortedColumns,
  displayRead: displayRead,
  displayEdit: displayEdit,
  displayDelete: displayDelete,
  actions: actions,
  apiEndpoint: apiEndpoint,
  idKeyPath: idKeyPath,
  listUIEndpoint: listUIEndpoint,
});

const overridenComponents = {
  ...defaultComponents,
  "ResultsList.item": SearchResultItemWithConfig,
};

createSearchAppInit(
  overridenComponents,
  true,
  "invenio-search-config",
  false,
  NotificationController
);
