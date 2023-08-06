import React from "react";
import { i18next } from "@translations/invenio_administration/i18next";
import { Sort, SearchBar } from "react-searchkit";
import PropTypes from "prop-types";

export const SearchResultOptions = ({ sortOptions, sortOrderDisabled }) => {
  return (
    <div className="auto-column-grid">
      <SearchBar />
      {sortOptions && (
        <Sort
          sortOrderDisabled={sortOrderDisabled}
          values={sortOptions}
          ariaLabel={i18next.t("Sort")}
          label={(cmp) => <>{cmp}</>} // eslint-disable-line react/jsx-no-useless-fragment
        />
      )}
    </div>
  );
};

SearchResultOptions.propTypes = {
  sortOptions: PropTypes.array.isRequired,
  sortOrderDisabled: PropTypes.bool,
};

SearchResultOptions.defaultProps = {
  sortOrderDisabled: false,
};
