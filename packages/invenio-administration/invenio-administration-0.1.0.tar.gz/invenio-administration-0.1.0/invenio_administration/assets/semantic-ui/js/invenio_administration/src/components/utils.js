import React, { Component } from "react";
import PropTypes from "prop-types";

export const sortFields = (schema) => {
  /**
   * Sort fields based on the order param supplied by view configuration
   * Doesn't take care of nested field - sorts only one level
   */
  return (
    Object.entries(schema)
      // sort by order
      .sort((a, b) => {
        if (a[1]?.ui && b[1].ui) {
          return a[1].ui.order > b[1].ui.order;
        }
        return true;
      })
      // build object with sorted attributes
      .reduce((sorted, entry) => {
        const key = entry[0];
        const fieldConfiguration = entry[1];
        sorted[key] = schema[key];

        sorted[key]["title"] = fieldConfiguration["text"] || schema[key].title;
        return sorted;
      }, {})
  );
};
