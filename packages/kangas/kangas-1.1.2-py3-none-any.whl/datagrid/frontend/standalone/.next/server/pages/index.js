"use strict";
(() => {
var exports = {};
exports.id = 405;
exports.ids = [405];
exports.modules = {

/***/ "@material-ui/icons":
/***/ ((module) => {

module.exports = require("@material-ui/icons");

/***/ }),

/***/ "./loadable":
/***/ ((module) => {

module.exports = require("next/dist/shared/lib/loadable.js");

/***/ }),

/***/ "react":
/***/ ((module) => {

module.exports = require("react");

/***/ }),

/***/ "react/jsx-runtime":
/***/ ((module) => {

module.exports = require("react/jsx-runtime");

/***/ }),

/***/ "(sc_server)/./pages/index.server.js":
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "__next_rsc__": () => (/* binding */ index_server_next_rsc_),
  "default": () => (/* binding */ index_server),
  "getServerSideProps": () => (/* binding */ getServerSideProps)
});

// EXTERNAL MODULE: external "react/jsx-runtime"
var jsx_runtime_ = __webpack_require__("react/jsx-runtime");
// EXTERNAL MODULE: external "react"
var external_react_ = __webpack_require__("react");
;// CONCATENATED MODULE: ./lib/useData.js
const cache = {};
function clearCache() {
    for(const key in cache){
        delete cache[key];
    }
}
function useData_useData(key, fetcher) {
    if (!cache[key]) {
        let data;
        let error;
        let promise;
        cache[key] = ()=>{
            if (error !== undefined || data !== undefined) return {
                data,
                error
            };
            if (!promise) {
                promise = fetcher().then((r)=>data = r)// Convert all errors to plain string for serialization
                .catch((e)=>error = e + "");
            }
            throw promise;
        };
    }
    return cache[key]();
}


;// CONCATENATED MODULE: ./config.js
// import { env } from 'node:process';
const localConfig = {
    apiKey: "",
    apiUrl: `http://localhost:${4001}/datagrid/`,
    useComet: false,
    defaultDecimalPrecision: 5
};
/* harmony default export */ const config_0 = (localConfig);

;// CONCATENATED MODULE: ./lib/fetchData.js

// Return type can be either json or blob, not case-sensitive
const fetchData_fetchData = async ({ url , query ={} , method ="POST" , returnType ="json"  })=>{
    const request = {
        method,
        headers: {
            // Authorization: config.apiKey,
            "Content-Type": "application/json"
        }
    };
    // Attaching a body to a GET request will throw an error
    if (method === "POST") request["body"] = JSON.stringify(query);
    // For GET requests, we have to parse the query into a url
    let getUrl = null;
    if (method === "GET") {
        const params = new URLSearchParams(query);
        getUrl = `${url}?${params.toString()}`;
    }
    const res = await fetch(getUrl || url, request);
    if (res.status !== 200) {
        throw new Error(`Status ${res.status}`);
    }
    if (returnType.toLowerCase() === "json") return res.json();
    if (returnType.toLowerCase() === "blob") return res.blob();
    if (returnType.toLowerCase() === "text") return res.text();
    throw `${returnType} is not a valid return type. Please choose either JSON or Blob`;
};
/* harmony default export */ const lib_fetchData = (fetchData_fetchData);

;// CONCATENATED MODULE: ./lib/fetchTable.js
// Config

// Utils

const fetchTable_fetchTable = async (query)=>{
    const data = await lib_fetchData({
        url: `${config_0.apiUrl}query`,
        query
    });
    // Can eventually implement transformations
    return data;
};
/* harmony default export */ const lib_fetchTable = (fetchTable_fetchTable);

;// CONCATENATED MODULE: external "node:buffer"
const external_node_buffer_namespaceObject = require("node:buffer");
;// CONCATENATED MODULE: ./lib/hashQuery.js

// Simple helper to generate a hash from a query object. We use this because
// our caching system, which is necessary to use React.Suspense, needs to assign a
// unique key to each distinct query.
const hashQuery_hashQuery = (query)=>{
    return external_node_buffer_namespaceObject.Buffer.from(JSON.stringify(query)).toString("base64");
};
/* harmony default export */ const lib_hashQuery = (hashQuery_hashQuery);

;// CONCATENATED MODULE: ./components/SettingsBar/GroupBy.client.js
const MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const GroupBy_client = ({ $$typeof: MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/SettingsBar/GroupBy.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/SettingsBar/MatrixSelect.client.js
const MatrixSelect_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const MatrixSelect_client = ({ $$typeof: MatrixSelect_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/SettingsBar/MatrixSelect.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/SettingsBar/SortBy.client.js
const SortBy_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const SortBy_client = ({ $$typeof: SortBy_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/SettingsBar/SortBy.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/SettingsBar/FilterExpr.client.js
const FilterExpr_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const FilterExpr_client = ({ $$typeof: FilterExpr_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/SettingsBar/FilterExpr.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Modals/DialogueModalContainer.client.js
const DialogueModalContainer_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const DialogueModalContainer_client = ({ $$typeof: DialogueModalContainer_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/Modals/DialogueModalContainer.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/SettingsBar/CustomizeColumns.client.js
const CustomizeColumns_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const CustomizeColumns_client = ({ $$typeof: CustomizeColumns_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/SettingsBar/CustomizeColumns.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/SettingsBar/PopoverModalContainer.client.js
const PopoverModalContainer_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const PopoverModalContainer_client = ({ $$typeof: PopoverModalContainer_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/SettingsBar/PopoverModalContainer.client.js", name: "default" });


// EXTERNAL MODULE: external "@material-ui/icons"
var icons_ = __webpack_require__("@material-ui/icons");
;// CONCATENATED MODULE: ./components/SettingsBar/Paging.client.js
const Paging_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const Paging_client = ({ $$typeof: Paging_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/SettingsBar/Paging.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/skeletons.js

function skeletons_Skeletons() {
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        children: "Loading"
    });
};

;// CONCATENATED MODULE: ./components/SettingsBar/SettingsBar.server.js


// Util



// Client Components










const SortButton = ()=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
        className: "button-outline",
        children: [
            /*#__PURE__*/ jsx_runtime_.jsx("img", {
                src: "/sort_icon.png"
            }),
            " ",
            /*#__PURE__*/ jsx_runtime_.jsx("span", {
                children: "Sort"
            })
        ]
    });
const GroupButton = ()=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
        className: "button-outline",
        children: [
            /*#__PURE__*/ jsx_runtime_.jsx("img", {
                src: "/group_placeholder.png"
            }),
            " ",
            /*#__PURE__*/ jsx_runtime_.jsx("span", {
                children: "Group by"
            })
        ]
    });
const SelectButton = ()=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
        className: "button-outline",
        children: [
            /*#__PURE__*/ jsx_runtime_.jsx("img", {
                src: "/columns_placeholder.png"
            }),
            " ",
            /*#__PURE__*/ jsx_runtime_.jsx("span", {
                children: "Columns"
            })
        ]
    });
const SelectRow = ({ columns , query , options  })=>{
    return /*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
        className: "select-row",
        children: [
            /*#__PURE__*/ jsx_runtime_.jsx(PopoverModalContainer_client, {
                toggleElement: /*#__PURE__*/ jsx_runtime_.jsx(GroupButton, {}),
                children: /*#__PURE__*/ jsx_runtime_.jsx(CustomizeColumns_client, {
                    query: query,
                    subtrees: [
                        "groupBy",
                        "sortBy"
                    ],
                    columns: columns
                })
            }),
            /*#__PURE__*/ jsx_runtime_.jsx(PopoverModalContainer_client, {
                toggleElement: /*#__PURE__*/ jsx_runtime_.jsx(SortButton, {}),
                children: /*#__PURE__*/ jsx_runtime_.jsx(CustomizeColumns_client, {
                    query: query,
                    subtree: "sortBy",
                    columns: columns
                })
            }),
            /*#__PURE__*/ jsx_runtime_.jsx(DialogueModalContainer_client, {
                toggleElement: /*#__PURE__*/ jsx_runtime_.jsx(SelectButton, {}),
                children: /*#__PURE__*/ jsx_runtime_.jsx(CustomizeColumns_client, {
                    query: query,
                    isMulti: true,
                    columns: columns,
                    defaultOptions: options
                })
            }),
            /*#__PURE__*/ jsx_runtime_.jsx(FilterExpr_client, {
                query: query
            })
        ]
    });
};
const SettingsBarServer = ({ query , matrices , columns , options  })=>{
    return /*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
        id: "settings-bar",
        children: [
            /*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                id: "matrix-select",
                className: "select-row",
                children: [
                    /*#__PURE__*/ jsx_runtime_.jsx("div", {
                        style: {
                            width: "auto"
                        },
                        children: /*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                            className: "button-outline",
                            children: [
                                /*#__PURE__*/ jsx_runtime_.jsx("img", {
                                    src: "/favicon.png"
                                }),
                                /*#__PURE__*/ jsx_runtime_.jsx("span", {
                                    children: "DataGrid"
                                })
                            ]
                        })
                    }),
                    /*#__PURE__*/ jsx_runtime_.jsx(MatrixSelect_client, {
                        query: query,
                        options: matrices
                    })
                ]
            }),
            /*#__PURE__*/ jsx_runtime_.jsx("div", {
                id: "nav-bar",
                children: /*#__PURE__*/ jsx_runtime_.jsx(SelectRow, {
                    columns: columns,
                    query: query,
                    options: options
                })
            })
        ]
    });
};
/* harmony default export */ const SettingsBar_server = (SettingsBarServer);

      const __next_rsc__ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/page.client.js
const page_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const page_client = ({ $$typeof: page_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/page.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/ExpandOverlay.client.js
const ExpandOverlay_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const ExpandOverlay_client = ({ $$typeof: ExpandOverlay_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/Cells/ExpandOverlay.client.js", name: "default" });


;// CONCATENATED MODULE: ./stubs.js
const STUB_QUERY_ARGS = {
    dgid: null,
    refresh: false,
    limit: 10
};
const STUB_MATRICES = (/* unused pure expression or super */ null && ([]));
const EMPTY_TABLE = {
    columns: [
        "row-id",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F"
    ],
    columnTypes: [
        "ROW_ID",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "PLACEHOLDER"
    ],
    nrows: 9,
    ncols: 8,
    total: 9,
    rows: [
        {
            "row-id": 1,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 2,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 3,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 4,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 5,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 6,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 7,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 8,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 9,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        }
    ]
};

// EXTERNAL MODULE: ./node_modules/next/dynamic.js
var dynamic = __webpack_require__("(sc_server)/./node_modules/next/dynamic.js");
;// CONCATENATED MODULE: ./components/ScrollProvider.client.js
const ScrollProvider_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const ScrollProvider_client = ({ $$typeof: ScrollProvider_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/ScrollProvider.client.js", name: "default" });


;// CONCATENATED MODULE: external "fs"
const external_fs_namespaceObject = require("fs");
;// CONCATENATED MODULE: ./lib/fetchAsset.js
// Config

// Utils


const fetchAsset_fetchAsset = async ({ assetId , dgid , returnUrl =false , returnType ="blob" , thumbnail =false  })=>{
    const data = await lib_fetchData({
        url: `${config_0.apiUrl}download`,
        query: {
            assetId,
            dgid,
            thumbnail
        },
        method: "GET",
        returnType
    });
    if (returnUrl) {
        const arrayBuffer = await data.arrayBuffer();
        const dataUrl = Buffer.from(arrayBuffer).toString("base64");
        return dataUrl;
    }
    return data;
};
/* harmony default export */ const lib_fetchAsset = (fetchAsset_fetchAsset);

// EXTERNAL MODULE: ./node_modules/next/image.js
var next_image = __webpack_require__("(sc_server)/./node_modules/next/image.js");
;// CONCATENATED MODULE: ./components/Cells/Image/ImageCell.server.js


// Config

// Utils



const ImageCell = ({ value , dgid  })=>{
    const { type , assetId , assetType  } = value;
    // Fetch this here, so it is available in the expanded view:
    const image = useData_useData(`${assetId}`, ()=>lib_fetchAsset({
            assetId,
            dgid,
            returnUrl: true
        }));
    const thumbnail = useData_useData(`${assetId}-thumbnail`, ()=>lib_fetchAsset({
            assetId,
            dgid,
            returnUrl: true,
            thumbnail: true
        }));
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content image",
        children: /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
            fallback: /*#__PURE__*/ jsx_runtime_.jsx("span", {
                children: "fallback"
            }),
            children: /*#__PURE__*/ jsx_runtime_.jsx(next_image/* default */.Z, {
                src: `data:application/octet-stream;base64,${thumbnail.data}`,
                layout: "fill",
                objectFit: "contain"
            })
        })
    });
};
/* harmony default export */ const ImageCell_server = (ImageCell);

      const ImageCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./lib/fetchAssetGroupThumbnail.js
// Config

// Utils

const fetchAssetGroupThumbnail = async ({ query  })=>{
    const data = await lib_fetchData({
        url: `${config_0.apiUrl}asset-group-thumbnail`,
        query,
        method: "POST",
        returnType: "blob"
    });
    const arrayBuffer = await data.arrayBuffer();
    const dataUrl = Buffer.from(arrayBuffer).toString("base64");
    return dataUrl;
};
/* harmony default export */ const lib_fetchAssetGroupThumbnail = (fetchAssetGroupThumbnail);

;// CONCATENATED MODULE: ./lib/fetchAssetGroup.js
// Config

// Utils



const fetchAssetGroup = async ({ query , returnUrl =false , returnType ="json" , size =0 , thumbnail =false  })=>{
    const data = await lib_fetchData({
        url: `${config_0.apiUrl}asset-group`,
        query,
        method: "POST",
        returnType
    });
    if (returnUrl && data?.values?.length) {
        const { dgid  } = query;
        const end = size ? size : data.values.length;
        const assetPromises = Promise.all(data.values.slice(0, end).map((assetId)=>{
            return lib_fetchAsset({
                assetId,
                dgid,
                returnUrl: true,
                thumbnail
            });
        })).then((dataUrls)=>dataUrls);
        return assetPromises;
    }
    return data;
};
/* harmony default export */ const lib_fetchAssetGroup = (fetchAssetGroup);

;// CONCATENATED MODULE: ./components/Cells/Image/Group.server.js


// Server Components

// Config

// Utils




const ImageGroupCell = ({ value , dgid  })=>{
    const query = {
        ...value,
        gallerySize: [
            3,
            2
        ],
        backgroundColor: [
            255,
            255,
            255
        ],
        imageSize: [
            100,
            55
        ],
        borderWidth: 2
    };
    // gallerySize is the number of columns, rows of the gallery image
    // imageSize is the max-width, max-height in pixels of each thumbnail image
    // in the gallery
    const countQuery = {
        ...value,
        columnLimit: 0
    };
    const groupThumbnail = useData_useData(`${lib_hashQuery(query)}`, ()=>lib_fetchAssetGroupThumbnail({
            query
        }));
    const groupDetails = useData_useData(`${lib_hashQuery(countQuery)}`, ()=>lib_fetchAssetGroup({
            query: countQuery
        }));
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content image-group",
        children: /*#__PURE__*/ (0,jsx_runtime_.jsxs)(external_react_.Suspense, {
            fallback: /*#__PURE__*/ jsx_runtime_.jsx("span", {
                children: "fallback"
            }),
            children: [
                /*#__PURE__*/ jsx_runtime_.jsx("span", {
                    children: `${groupDetails.data.total} Images`
                }),
                /*#__PURE__*/ jsx_runtime_.jsx(next_image/* default */.Z, {
                    src: `data:application/octet-stream;base64,${groupThumbnail.data}`,
                    layout: "fill",
                    objectFit: "contain"
                })
            ]
        })
    });
};
/* harmony default export */ const Group_server = (ImageGroupCell);

      const Group_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/Image/ImageCanvas.client.js
const ImageCanvas_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const ImageCanvas_client = ({ $$typeof: ImageCanvas_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/Cells/Image/ImageCanvas.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/Image/Expanded.server.js


// Config

// Client

const ExpandedImageCell = ({ value , dgid , row , col  })=>{
    const { type , assetId , assetType  } = value;
    const url = `${config_0.apiUrl}download?assetId=${assetId}&dgid=${dgid}`;
    const metadata = typeof row !== "undefined" ? row[`${col}--metadata`] : null;
    return /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
        fallback: /*#__PURE__*/ jsx_runtime_.jsx(jsx_runtime_.Fragment, {
            children: "Loading"
        }),
        children: /*#__PURE__*/ jsx_runtime_.jsx(ImageCanvas_client, {
            url: url,
            metadata: metadata,
            dgid: dgid,
            assetId: assetId
        })
    });
};
/* harmony default export */ const Expanded_server = (ExpandedImageCell);

      const Expanded_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/Image/Image.server.js


// Config

// Utils


const Image = ({ assetId , dgid  })=>{
    const image = useData(`${assetId}`, ()=>fetchAsset({
            assetId,
            dgid,
            returnUrl: true
        }));
    return /*#__PURE__*/ _jsx(Suspense, {
        fallback: /*#__PURE__*/ _jsx("span", {
            children: "fallback"
        }),
        children: /*#__PURE__*/ _jsx("img", {
            src: `data:application/octet-stream;base64,${image.data}`
        })
    });
};
/* harmony default export */ const Image_server = ((/* unused pure expression or super */ null && (Image)));

      const Image_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/Image/LazyImageGroup.client.js
const LazyImageGroup_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const LazyImageGroup_client = ({ $$typeof: LazyImageGroup_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/Cells/Image/LazyImageGroup.client.js", name: "default" });


;// CONCATENATED MODULE: ./lib/cometAssetURL.js

const cometAssetURL = ({ assetId , assetType , type , experimentKey  })=>{
    const url = new URL(`${config.assetUrl}download?experimentKey=${experimentKey}&assetId=${assetId}`);
    return {
        src: url.href
    };
};
/* harmony default export */ const lib_cometAssetURL = ((/* unused pure expression or super */ null && (cometAssetURL)));

;// CONCATENATED MODULE: ./components/Cells/Image/ExpandedGroup.server.js


// Server Components

// Client Components

// Config

// Util




const ExpandedGroupImageCell = ({ value , dgid  })=>{
    const images = useData_useData(`${lib_hashQuery(value)}`, ()=>lib_fetchAssetGroup({
            query: value,
            thumbnail: true
        })).data;
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content expanded image",
        children: /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
            fallback: /*#__PURE__*/ jsx_runtime_.jsx(jsx_runtime_.Fragment, {
                children: "loading"
            }),
            children: /*#__PURE__*/ jsx_runtime_.jsx(LazyImageGroup_client, {
                images: images,
                dgid: dgid
            })
        })
    });
};
/* harmony default export */ const ExpandedGroup_server = (ExpandedGroupImageCell);

      const ExpandedGroup_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./lib/truncateValue.js
// Config

const countDecimals = (value)=>{
    if (Math.floor(value) === value) return 0;
    const [, decimalPart = ""] = value.toString().split(".");
    return decimalPart.length;
};
const truncateValue = (value, customDecimalsPrecision)=>{
    const decimalsPrecision = customDecimalsPrecision ?? config_0.defaultDecimalPrecision;
    if (decimalsPrecision === null) return value;
    const numberValue = Number(value);
    if (isNaN(numberValue)) return value;
    if (Number.isInteger(numberValue) || countDecimals(numberValue) <= decimalsPrecision) {
        return numberValue;
    }
    const exponential = 10 ** decimalsPrecision;
    return Math.floor(numberValue * exponential) / exponential;
};
/* harmony default export */ const lib_truncateValue = (truncateValue);

;// CONCATENATED MODULE: ./lib/formatValue.js

function formatValue(value, columnType) {
    if (value === null) {
        return "None";
    }
    let retval = value;
    if (columnType === "DATETIME") {
        const timestampObj = new UnixTime(value);
        retval = timestampObj.format("YYYY-MM-DD HH:mm:ss");
    } else if (columnType === "FLOAT") {
        retval = lib_truncateValue(value).toString();
    } else if (typeof value !== "string") {
        retval = value.toString();
    }
    return retval;
}
function pad(item, size, padding = "0") {
    return String(item).padStart(size, padding);
}
class UnixTime {
    constructor(datetime){
        this.obj = new Date(datetime * 1000);
        this.year = pad(this.obj.getFullYear(), 4);
        this.month = pad(this.obj.getDate(), 2);
        this.day = pad(this.obj.getDate(), 2);
        this.hour = pad(this.obj.getHours(), 2);
        this.minute = pad(this.obj.getMinutes(), 2);
        this.second = pad(this.obj.getSeconds(), 2);
    }
    format(string) {
        // Hard coded for now: 'YYYY-MM-DD HH:mm:ss'
        if (this.hour === "00" && this.minute === "00" && this.second === "00") {
            return `${this.year}-${this.month}-${this.day}`;
        } else {
            return `${this.year}-${this.month}-${this.day} ${this.hour}:${this.minute}:${this.second}`;
        }
    }
}
/* harmony default export */ const lib_formatValue = (formatValue);

;// CONCATENATED MODULE: ./components/Cells/DateCell.server.js


const DateCell = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content",
        children: `${lib_formatValue(value, "DATETIME")}`
    });
};
/* harmony default export */ const DateCell_server = (DateCell);

      const DateCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/TextCell.server.js


const TextCell = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content",
        children: `${lib_formatValue(value, "TEXT")}`
    });
};
/* harmony default export */ const TextCell_server = (TextCell);

      const TextCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/FloatCell.server.js

// Utils

const FloatCell = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content",
        children: `${lib_formatValue(value, "FLOAT")}`
    });
};
/* harmony default export */ const FloatCell_server = (FloatCell);

      const FloatCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/FloatExpanded.server.js

// Config

const FloatExpanded = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content",
        children: `${value}`
    });
};
/* harmony default export */ const FloatExpanded_server = (FloatExpanded);

      const FloatExpanded_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/AudioCell.server.js

// Config

// Client components
//import Player from '../Player/Player.client';
// Util



// To get our fun waveform effect, we need to implement something better than wavesurfer.js. For now, the native
// audio element works fantastic. Users can control playback, skip around, etc.
const AudioCell = ({ value , dgid  })=>{
    const { type , assetId , assetType  } = value;
    const image = useData_useData(`${assetId}`, ()=>lib_fetchAsset({
            assetId,
            dgid
        }));
    // Wavesurfer is going to be difficult with SSR. Need to reconfigure.
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content audio",
        children: /*#__PURE__*/ jsx_runtime_.jsx("audio", {
            src: "",
            controls: true
        })
    });
/*
    return (
        <Player
        src={`${cell.src}`}
        style={{ width: '100%' }}
        height={90}
        />
    )*/ };
/* harmony default export */ const AudioCell_server = (AudioCell);

      const AudioCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/VideoCell.server.js

// Config

// Util



/* In comet-react, we use react-player, which gives us out of the box support for YouTube/Vimeo/Wistia links etc.
However, it is also heavy and completely client side. The question is: How big is that use case? How often are users
logging links to 3rd party video platforms as part of their data vs. logging actual video files? */ const VideoCell = ({ value , dgid  })=>{
    const { type , assetId , assetType  } = value;
    //const video = useData(`${assetId}`, () => fetchAsset({ assetId, dgid, returnUrl: true}));
    const video_url = `${config_0.apiUrl}download?assetId=${assetId}&dgid=${dgid}`;
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content video",
        children: /*#__PURE__*/ jsx_runtime_.jsx("video", {
            src: video_url,
            controls: true
        })
    });
};
/* harmony default export */ const VideoCell_server = (VideoCell);

      const VideoCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/TextAssetCell.server.js

// Config

// Util




// import hljs from 'highlight.js';
// In comet-react, we use highlight.js to render text. This is not a problem for RSC—highlight.js works on the server—but it's
// not clear why we actually use highlight in comet-react. The point of highlight is that it can provide formatting for a variety
// of text formats (different programming languages, in particular), but we have hardcoded the language to "plaintext" in comet-react
const TextAssetCell = ({ value , dgid  })=>{
    const { type , assetId , assetType  } = value;
    const image = useData_useData(`${assetId}`, ()=>lib_fetchAsset({
            assetId,
            dgid
        }));
    // const asset = useData(`${cell.src}`, () => fetchData({url: cell.src, method: 'GET', returnType: 'blob'}).then(blob => blob.text()));
    // const { data: text, error } = asset;
    // const parsed = hljs.highlightAuto(text);
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content text-asset",
        children: /*#__PURE__*/ jsx_runtime_.jsx("pre", {
            children: /*#__PURE__*/ jsx_runtime_.jsx("code", {
                children: "text"
            })
        })
    });
};
/* harmony default export */ const TextAssetCell_server = (TextAssetCell);

      const TextAssetCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/CurveAssetCell.client.js
const CurveAssetCell_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const CurveAssetCell_client = ({ $$typeof: CurveAssetCell_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/Cells/CurveAssetCell.client.js", name: "default" });


;// CONCATENATED MODULE: ./lib/generateChartColor.js
// Color functions
const getUniqueColor = (n)=>{
    // Must return lowercase hex
    // so that getContrastingColor will work
    const rgb = [
        0,
        0,
        0
    ];
    let counter = n;
    for(let i = 0; i < 24; i++){
        rgb[i % 3] <<= 1;
        rgb[i % 3] |= counter & 0x01;
        counter >>= 1;
    }
    return `#${rgb.reduce((a, c)=>(c > 0x0f ? c.toString(16) : `0${c.toString(16)}`) + a, "")}`;
};
const getColor = (text = "0")=>{
    // Must return lowercase hex
    // so that getContrastingColor will work
    if (text === "1") return "#228b22"; // forest green
    if (text === "0") return "#ff3131"; // neon red
    const hash = [
        ...text
    ].reduce((acc, char)=>{
        return char.charCodeAt(0) + ((acc << 5) - acc);
    }, 0);
    return getUniqueColor(hash % 1024);
};
const hexToRgb = (hex)=>{
    const result = hex.match(/^#([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/);
    return [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16)
    ];
};
const getContrastingColor = (hex)=>{
    const colors = hexToRgb(hex);
    const r = colors[0];
    const g = colors[1];
    const b = colors[2];
    const o = Math.round((r * 299 + g * 587 + b * 114) / 1000);
    return o > 125 ? "black" : "white";
};

;// CONCATENATED MODULE: ./components/Cells/CurveAssetCell.server.js

// Client components

// Util



// TODO Create a helper called generateLayout that also generates data.
const CurveAssetCellServer = ({ value , dgid  })=>{
    const { type , assetId , assetType  } = value;
    const asset = useData_useData(`${assetId}`, ()=>lib_fetchAsset({
            assetId,
            dgid,
            returnType: "json"
        }));
    const { data , error  } = asset;
    const chartData = [
        {
            type: "line",
            x: data.x,
            y: data.y,
            marker: {
                color: getColor(data.name)
            }
        }
    ];
    const layout = {
        paper_bgcolor: "white",
        plot_bgcolor: "white",
        width: 120,
        height: 120,
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
            pad: 0
        },
        showlegend: false,
        xaxis: {
            visible: false,
            showticklabels: false
        },
        yaxis: {
            visible: false,
            showticklabels: false
        }
    };
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content curve-asset",
        children: /*#__PURE__*/ jsx_runtime_.jsx(CurveAssetCell_client, {
            chartData: chartData,
            layout: layout
        })
    });
};
/* harmony default export */ const CurveAssetCell_server = (CurveAssetCellServer);

      const CurveAssetCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/BooleanCell.client.js
const BooleanCell_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const BooleanCell_client = ({ $$typeof: BooleanCell_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/Cells/BooleanCell.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/BooleanCell.server.js

// Client components

const BooleanCell = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content boolean",
        children: /*#__PURE__*/ jsx_runtime_.jsx(BooleanCell_client, {
            sign: value === 1
        })
    });
};
/* harmony default export */ const BooleanCell_server = (BooleanCell);

      const BooleanCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/JSONCell.server.js

const JSONCell = ({ value  })=>{
    let jsonValue;
    try {
        jsonValue = JSON.parse(value);
    } catch  {
        jsonValue = {
            ERROR: `expecting JSON but got '${value}'`
        };
    }
    const strValue = Object.keys(jsonValue).filter((key)=>[
            "string",
            "number",
            "boolean"
        ].includes(typeof key)).map((key)=>`${key}: ${jsonValue[key]}`).join(", ");
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content json",
        children: strValue
    });
};
/* harmony default export */ const JSONCell_server = (JSONCell);

      const JSONCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/PlaceholderCell.server.js

const PlaceholderCell = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "placeholder-cell"
    });
};
/* harmony default export */ const PlaceholderCell_server = (PlaceholderCell);

      const PlaceholderCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/Histogram/HistogramGroupCell.client.js
const HistogramGroupCell_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const HistogramGroupCell_client = ({ $$typeof: HistogramGroupCell_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/Cells/Histogram/HistogramGroupCell.client.js", name: "default" });


;// CONCATENATED MODULE: ./lib/fetchHistogram.js
// Config

// Utils


const fetchHistogram = async ({ query  })=>{
    const data = await fetchData({
        url: `${config.apiUrl}histogram`,
        query,
        method: "POST"
    });
    return data;
};
/* harmony default export */ const lib_fetchHistogram = ((/* unused pure expression or super */ null && (fetchHistogram)));

;// CONCATENATED MODULE: ./components/DeferredCell.client.js
const DeferredCell_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const DeferredCell_client = ({ $$typeof: DeferredCell_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/DeferredCell.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/Histogram/HistogramGroupCell.server.js


// Client components

// Util





// TODO Create a helper called generateLayout that also generates data.
const HistogramGroupCell = ({ value , dgid  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content histogram",
        children: /*#__PURE__*/ jsx_runtime_.jsx(DeferredCell_client, {
            children: /*#__PURE__*/ jsx_runtime_.jsx(HistogramGroupCell_client, {
                value: value
            })
        })
    });
};
/* harmony default export */ const HistogramGroupCell_server = (HistogramGroupCell);

      const HistogramGroupCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/Histogram/HistogramGroupExpanded.client.js
const HistogramGroupExpanded_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const HistogramGroupExpanded_client = ({ $$typeof: HistogramGroupExpanded_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/Cells/Histogram/HistogramGroupExpanded.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/Histogram/HistogramGroupExpanded.server.js


const HistogramGroupExpanded = ({ value , dgid  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content histogram",
        children: /*#__PURE__*/ jsx_runtime_.jsx(HistogramGroupExpanded_client, {
            value: value
        })
    });
};
/* harmony default export */ const HistogramGroupExpanded_server = (HistogramGroupExpanded);

      const HistogramGroupExpanded_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/Category/CategoryGroupCell.client.js
const CategoryGroupCell_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const CategoryGroupCell_client = ({ $$typeof: CategoryGroupCell_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/Cells/Category/CategoryGroupCell.client.js", name: "default" });


;// CONCATENATED MODULE: ./lib/fetchCategory.js
// Config

// Utils


const fetchCategory = async ({ query  })=>{
    const data = await fetchData({
        url: `${config.apiUrl}category`,
        query,
        method: "POST"
    });
    return data;
};
/* harmony default export */ const lib_fetchCategory = ((/* unused pure expression or super */ null && (fetchCategory)));

;// CONCATENATED MODULE: ./components/Cells/Category/CategoryGroupCell.server.js


// Client components


// Util





// TODO Create a helper called generateLayout that also generates data.
const CategoryGroupCell = ({ value , dgid ,  })=>/*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content curve-asset",
        children: /*#__PURE__*/ jsx_runtime_.jsx(DeferredCell_client, {
            children: /*#__PURE__*/ jsx_runtime_.jsx(CategoryGroupCell_client, {
                value: value
            })
        })
    });
/* harmony default export */ const CategoryGroupCell_server = (CategoryGroupCell);

      const CategoryGroupCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/Cells/Category/CategoryGroupExpanded.client.js
const CategoryGroupExpanded_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const CategoryGroupExpanded_client = ({ $$typeof: CategoryGroupExpanded_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/Cells/Category/CategoryGroupExpanded.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/Category/CategoryGroupExpanded.server.js


// Client components

// Util





// TODO Create a helper called generateLayout that also generates data.
const CategoryGroupExpanded_server_CategoryGroupCell = ({ value , dgid  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content curve-asset",
        children: /*#__PURE__*/ jsx_runtime_.jsx(CategoryGroupExpanded_client, {
            value: value
        })
    });
};
/* harmony default export */ const CategoryGroupExpanded_server = (CategoryGroupExpanded_server_CategoryGroupCell);

      const CategoryGroupExpanded_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./lib/makeComponentMap.js




















const SINGLE_VALUE_WIDTH = 75;
const GROUPED_ASSET_WIDTH = 150;
const makeComponentMap_columnTypeMap = {
    BOOLEAN: {
        component: BooleanCell_server,
        expandedComponent: BooleanCell_server,
        groupComponent: BooleanCell_server,
        expandedGroupComponent: BooleanCell_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH
    },
    TEXT: {
        component: TextCell_server,
        expandedComponent: TextCell_server,
        groupComponent: CategoryGroupCell_server,
        expandedGroupComponent: CategoryGroupExpanded_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH
    },
    INTEGER: {
        component: TextCell_server,
        expandedComponent: TextCell_server,
        groupComponent: CategoryGroupCell_server,
        expandedGroupComponent: CategoryGroupExpanded_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH
    },
    FLOAT: {
        component: FloatCell_server,
        expandedComponent: FloatExpanded_server,
        groupComponent: HistogramGroupCell_server,
        expandedGroupComponent: HistogramGroupExpanded_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH
    },
    DATETIME: {
        component: DateCell_server,
        expandedComponent: DateCell_server,
        groupComponent: HistogramGroupCell_server,
        expandedGroupComponent: HistogramGroupExpanded_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH
    },
    JSON: {
        component: JSONCell_server,
        expandedComponent: JSONCell_server,
        groupComponent: JSONCell_server,
        expandedGroupComponent: JSONCell_server,
        singleWidth: 300,
        groupedWidth: 300
    },
    ROW_ID: {
        component: TextCell_server,
        expandedComponent: TextCell_server,
        groupComponent: PlaceholderCell_server,
        expandedGroupComponent: PlaceholderCell_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: SINGLE_VALUE_WIDTH
    },
    "IMAGE-ASSET": {
        component: ImageCell_server,
        expandedComponent: Expanded_server,
        groupComponent: Group_server,
        expandedGroupComponent: ExpandedGroup_server,
        singleWidth: SINGLE_VALUE_WIDTH * 2,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: true
    },
    "AUDIO-ASSET": {
        component: AudioCell_server,
        expandedComponent: AudioCell_server,
        groupComponent: AudioCell_server,
        expandedGroupComponent: AudioCell_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: true
    },
    "CURVE-ASSET": {
        component: CurveAssetCell_server,
        expandedComponent: CurveAssetCell_server,
        groupComponent: CurveAssetCell_server,
        expandedGroupComponent: CurveAssetCell_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: true
    },
    "TEXT-ASSET": {
        component: TextAssetCell_server,
        expandedComponent: TextAssetCell_server,
        groupComponent: TextAssetCell_server,
        expandedGroupComponent: TextAssetCell_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: true
    },
    "VIDEO-ASSET": {
        component: VideoCell_server,
        expandedComponent: VideoCell_server,
        groupComponent: VideoCell_server,
        expandedGroupComponent: VideoCell_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: true
    },
    "PLACEHOLDER": {
        component: PlaceholderCell_server,
        expandedComponent: PlaceholderCell_server,
        groupComponent: PlaceholderCell_server,
        expandedGroupComponent: PlaceholderCell_server,
        singleWidth: SINGLE_VALUE_WIDTH * 2,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: false
    }
};
const makeComponentMap = (table)=>{
    const { columnTypes , columns , ncols  } = table;
    // Make sure our columns aren't foo-bar'd
    if (!columns || columns.length !== ncols) return null;
    const nameToComponent = {};
    columns.forEach((name, idx)=>{
        const type = columnTypes[idx];
        nameToComponent[name] = {
            component: makeComponentMap_columnTypeMap[type].component,
            type,
            accessor: name,
            idx,
            singleWidth: makeComponentMap_columnTypeMap[type].singleWidth,
            groupedWidth: makeComponentMap_columnTypeMap[type].groupedWidth,
            isAsset: makeComponentMap_columnTypeMap[type].isAsset
        };
    });
    return nameToComponent;
};
/* harmony default export */ const lib_makeComponentMap = ((/* unused pure expression or super */ null && (makeComponentMap)));

;// CONCATENATED MODULE: ./components/RowBlock.server.js


// Client Components


// Util


const RowBlock_server_RowBlock = ({ rows , columns , columnTypes , dgid , total  })=>{
    return /*#__PURE__*/ _jsx(ScrollProvider, {
        children: rows.map((row, ridx)=>/*#__PURE__*/ _jsx("div", {
                className: "row",
                children: columns.map((col, idx)=>/*#__PURE__*/ _jsxs("div", {
                        className: "column cell",
                        children: [
                            columnTypeMap[columnTypes[idx]].component({
                                value: row[col],
                                dgid,
                                row,
                                col
                            }),
                            /*#__PURE__*/ _jsx(ExpandOverlay, {
                                children: columnTypeMap[columnTypes[idx]].expandedComponent({
                                    value: row[col],
                                    dgid,
                                    row,
                                    col
                                })
                            })
                        ]
                    }, `${ridx}-${idx}`))
            }, `row-${ridx}`))
    });
};
/* harmony default export */ const RowBlock_server = ((/* unused pure expression or super */ null && (RowBlock_server_RowBlock)));

      const RowBlock_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/VanillaTable.server.js




// Server Components
// const RowBlock = dynamic(() => import('./RowBlock.server'), { suspense: true });

// Client Components

// Util





// The rendering is messy but WIP
const VanillaTable = ({ query , groupBy  })=>{
    const { data: table , tableError  } = useData(`query-${hashQuery({
        query
    })}`, ()=>fetchTable(query));
    const { columnTypes , columns =[] , ncols , nrows , rows =[]  } = table ?? {};
    const filteredColumns = columns.filter((name)=>!name.endsWith("--metadata"));
    return /*#__PURE__*/ _jsx(Suspense, {
        fallback: /*#__PURE__*/ _jsx(Skeletons, {}),
        children: /*#__PURE__*/ _jsxs("div", {
            className: "table-root",
            children: [
                /*#__PURE__*/ _jsx("div", {
                    id: "header-row",
                    className: "row",
                    children: filteredColumns.map((col)=>/*#__PURE__*/ _jsx("div", {
                            className: "column",
                            children: col
                        }))
                }),
                /*#__PURE__*/ _jsx(Suspense, {
                    fallback: /*#__PURE__*/ _jsx(Skeletons, {}),
                    children: /*#__PURE__*/ _jsx(RowBlock, {
                        rows: rows.slice(0, 15),
                        columns: filteredColumns,
                        columnTypes: columnTypes,
                        dgid: query?.dgid
                    })
                }),
                /*#__PURE__*/ _jsx(Suspense, {
                    fallback: /*#__PURE__*/ _jsx(Skeletons, {}),
                    children: /*#__PURE__*/ _jsx(RowBlock, {
                        rows: rows.slice(15, 1000),
                        columns: filteredColumns,
                        columnTypes: columnTypes,
                        dgid: query?.dgid
                    })
                })
            ]
        })
    });
};
/* harmony default export */ const VanillaTable_server = ((/* unused pure expression or super */ null && (VanillaTable)));

      const VanillaTable_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/FooterRow.server.js


const FooterRow = ({ query , total  })=>{
    const pages = Math.ceil(total / (query?.limit || total));
    const pagination = Array.from({
        length: pages
    }, (val, idx)=>idx + 1);
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "footer-row",
        children: /*#__PURE__*/ jsx_runtime_.jsx(Paging_client, {
            query: query,
            total: total,
            pagination: pagination
        })
    });
};
/* harmony default export */ const FooterRow_server = (FooterRow);

      const FooterRow_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }

;// CONCATENATED MODULE: ./components/SettingsBar/Imports.client.js
const Imports_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const Imports_client = ({ $$typeof: Imports_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/comet-datagrid/components/SettingsBar/Imports.client.js", name: "default" });


;// CONCATENATED MODULE: ./pages/index.server.js


// Server Components

// Client Components


// Utils












// For now, this page is essentially our root
const Root = ({ query , matrices  })=>{
    const { data: table , tableError  } = useData_useData(`query-${lib_hashQuery({
        query
    })}`, ()=>lib_fetchTable(query));
    const { data: allColumns , colError  } = useData_useData(`query-${lib_hashQuery({
        query: {
            ...query,
            select: "*",
            limit: 1
        }
    })}`, ()=>lib_fetchTable(query));
    const { dgid , limit  } = query;
    const { columnTypes , columns , ncols , nrows , rows , total  } = table ?? EMPTY_TABLE;
    const columnOptions = !!allColumns ? Object.keys(allColumns?.rows[0]).filter((col)=>!col.endsWith("--metadata")) : [];
    // TODO Clean this up with .filter()
    const filteredColumns = [];
    const filteredColumnTypes = [];
    columns.forEach((columnName, idx)=>{
        if (!columnName.endsWith("--metadata")) {
            filteredColumnTypes.push(columnTypes[idx]);
            filteredColumns.push(columnName);
        }
    });
    const ready = !!table && !!columns && !!dgid;
    // TODO Clean up
    const rowClass = !!query?.groupBy && query?.groupBy ? "row-group" : "row";
    const colClass = !!query?.groupBy && query?.groupBy ? "column-group cell-group" : "column cell";
    const headerClass = colClass.includes("group") ? "column-group" : "column";
    return /*#__PURE__*/ (0,jsx_runtime_.jsxs)(page_client, {
        children: [
            /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
                fallback: /*#__PURE__*/ jsx_runtime_.jsx(skeletons_Skeletons, {}),
                children: /*#__PURE__*/ jsx_runtime_.jsx(Imports_client, {})
            }),
            /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
                fallback: /*#__PURE__*/ jsx_runtime_.jsx(skeletons_Skeletons, {}),
                children: /*#__PURE__*/ jsx_runtime_.jsx(SettingsBar_server, {
                    query: query,
                    matrices: matrices,
                    columns: filteredColumns,
                    options: columnOptions
                })
            }),
            /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
                fallback: /*#__PURE__*/ jsx_runtime_.jsx(skeletons_Skeletons, {}),
                children: /*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                    className: "table-root",
                    children: [
                        /*#__PURE__*/ jsx_runtime_.jsx("div", {
                            id: "header-row",
                            className: `${rowClass}`,
                            children: filteredColumns.map((col)=>/*#__PURE__*/ jsx_runtime_.jsx("div", {
                                    className: headerClass,
                                    title: col,
                                    children: col
                                }))
                        }),
                        rows.map((row, ridx)=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                                className: `${rowClass}`,
                                children: [
                                    filteredColumns.slice(0, 5).map((col, idx)=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                                            className: `${colClass}`,
                                            children: [
                                                !!query?.groupBy && query?.groupBy !== col ? makeComponentMap_columnTypeMap[filteredColumnTypes[idx]].groupComponent({
                                                    value: row[col],
                                                    dgid,
                                                    row,
                                                    col
                                                }) : makeComponentMap_columnTypeMap[filteredColumnTypes[idx]].component({
                                                    value: row[col],
                                                    dgid,
                                                    row,
                                                    col
                                                }),
                                                /*#__PURE__*/ jsx_runtime_.jsx(ExpandOverlay_client, {
                                                    children: !!query?.groupBy && query?.groupBy !== col ? makeComponentMap_columnTypeMap[filteredColumnTypes[idx]].expandedGroupComponent({
                                                        value: row[col],
                                                        dgid,
                                                        row,
                                                        col
                                                    }) : makeComponentMap_columnTypeMap[filteredColumnTypes[idx]].expandedComponent({
                                                        value: row[col],
                                                        dgid,
                                                        row,
                                                        col
                                                    })
                                                })
                                            ]
                                        }, `${ridx}-${idx}`)),
                                    filteredColumns.length > 5 && filteredColumns.slice(5).map((col, idx)=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                                            className: `${colClass}`,
                                            children: [
                                                !!query?.groupBy && query?.groupBy !== col ? makeComponentMap_columnTypeMap[filteredColumnTypes[idx + 5]].groupComponent({
                                                    value: row[col],
                                                    dgid,
                                                    row,
                                                    col,
                                                    defer: true
                                                }) : makeComponentMap_columnTypeMap[filteredColumnTypes[idx + 5]].component({
                                                    value: row[col],
                                                    dgid,
                                                    row,
                                                    col
                                                }),
                                                /*#__PURE__*/ jsx_runtime_.jsx(ExpandOverlay_client, {
                                                    children: !!query?.groupBy && query?.groupBy !== col ? makeComponentMap_columnTypeMap[filteredColumnTypes[idx + 5]].expandedGroupComponent({
                                                        value: row[col],
                                                        dgid,
                                                        row,
                                                        col,
                                                        defer: true
                                                    }) : makeComponentMap_columnTypeMap[filteredColumnTypes[idx + 5]].expandedComponent({
                                                        value: row[col],
                                                        dgid,
                                                        row,
                                                        col
                                                    })
                                                })
                                            ]
                                        }, `${ridx}-${idx + 5}`))
                                ]
                            }, `row-${ridx}`))
                    ]
                })
            }),
            /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
                fallback: /*#__PURE__*/ jsx_runtime_.jsx(skeletons_Skeletons, {}),
                children: /*#__PURE__*/ jsx_runtime_.jsx(FooterRow_server, {
                    query: query,
                    total: total
                })
            })
        ]
    });
};
// The Next.js server knows to look for this function and apply it to the index.server page
const getServerSideProps = async (context)=>{
    const data = await fetch(`${config_0.apiUrl}list`);
    const matrices = await data.json();
    return {
        props: {
            matrices: matrices || [],
            query: {
                dgid: context.query?.datagrid || null,
                limit: 10
            }
        }
    };
};
/* harmony default export */ const index_server = (Root); /*

          <RowBlock rows={rows.slice(0, 50)} columns={filteredColumns} columnTypes={columnTypes} query={query} block={0} />
          <RowBlock rows={rows.slice(-150, -149)} columns={filteredColumns} columnTypes={columnTypes} query={query} block={1} />
          <RowBlock rows={rows.slice(-149, -50)} columns={filteredColumns} columnTypes={columnTypes} query={query} block={2} />
          <ScrollProvider query={query} total={total}>
            <RowBlock rows={rows.slice(-50, -49)} columns={filteredColumns} columnTypes={columnTypes} query={query} block={3} />
          </ScrollProvider>
          <RowBlock rows={rows.slice(-49)} columns={filteredColumns} columnTypes={columnTypes} query={query} block={4} />

          */  /*             <RowBlock rows={rows.slice(0, -100)} columns={filteredColumns} columnTypes={columnTypes} query={query} block={0} />
            <ScrollProvider query={query} block={1} total={total}>
              <RowBlock rows={rows.slice(-100, -99)} columns={filteredColumns} columnTypes={columnTypes} query={query} block={1} />
            </ScrollProvider>
            <RowBlock rows={rows.slice(-99)} columns={filteredColumns} columnTypes={columnTypes} query={query} block={2} />
*/

      const index_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }


/***/ })

};
;

// load runtime
var __webpack_require__ = require("../webpack-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = __webpack_require__.X(0, [546], () => (__webpack_exec__("(sc_server)/./pages/index.server.js")));
module.exports = __webpack_exports__;

})();