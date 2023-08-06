"use strict";
(self["webpackChunkomoujan"] = self["webpackChunkomoujan"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! axios */ "webpack/sharing/consume/default/axios/axios");
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(axios__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _config_config_json__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./config/config.json */ "./lib/config/config.json");
/* harmony import */ var _config_user_config_json__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./config/user_config.json */ "./lib/config/user_config.json");






const API_URL = _config_config_json__WEBPACK_IMPORTED_MODULE_4__.api_root_url + _config_config_json__WEBPACK_IMPORTED_MODULE_4__.api_reccomend;
const extension = {
    id: 'creative',
    autoStart: true,
    optional: [],
    requires: [],
    activate,
};
function activate(app) {
    const { shell } = app;
    // Call function after finish executing cell
    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookActions.executed.connect((_, action) => {
        // console.log("action: ", action)
        if (action.success) {
            // console.log("action.success", action.success)
        }
        else {
            // console.log("action.success", action.success)
            // console.log("action.error", action.error)
            let headers = {
                "accept": "application/json",
                "Content-Type": "application/json"
            };
            // console.log("user_config: ", user_config)
            // console.log("config: ", config)
            let request_data = _config_user_config_json__WEBPACK_IMPORTED_MODULE_5__;
            request_data['code_text'] = 'string';
            request_data['output_text'] = '';
            request_data['error_text'] = String(action.error);
            // console.log("request_data: ", request_data)
            // Post data
            axios__WEBPACK_IMPORTED_MODULE_0___default().post(API_URL, request_data, { headers: headers }).then(({ data }) => {
                // console.log("data: ", data)
                // const widget = createWidget(data)
                createWidget(data);
                // console.log('widget: ', widget)
            });
        }
    });
    function createWidget(data) {
        var _a, _b, _c, _d;
        let url_first = data.result[0].url;
        let img_first = data.result[0].img_base64;
        let url_second = data.result[1].url;
        let img_second = data.result[1].img_base64;
        let url_third = data.result[2].url;
        let img_third = data.result[2].img_base64;
        //
        let img_tag_first = document.createElement('img');
        img_tag_first.src = "data:image/gif;base64," + img_first;
        img_tag_first.style.width = "100%";
        // set elems
        let a_tag_first = document.createElement('a');
        a_tag_first.href = url_first;
        a_tag_first.rel = "noopener";
        a_tag_first.target = "_blank";
        // set styles
        a_tag_first.style.width = "32%";
        a_tag_first.style.height = "fit-content";
        a_tag_first.style.color = "white";
        a_tag_first.style.fontFamily = "JetBrains Mono";
        let img_tag_second = document.createElement('img');
        img_tag_second.src = "data:image/gif;base64," + img_second;
        img_tag_second.style.width = "100%";
        let a_tag_second = document.createElement('a');
        a_tag_second.href = url_second;
        a_tag_second.rel = "noopener";
        a_tag_second.target = "_blank";
        // set styles
        a_tag_second.style.width = "32%";
        a_tag_second.style.height = "fit-content";
        a_tag_second.style.color = "white";
        a_tag_second.style.fontFamily = "JetBrains Mono";
        let img_tag_third = document.createElement('img');
        img_tag_third.src = "data:image/gif;base64," + img_third;
        img_tag_third.style.width = "100%";
        let a_tag_third = document.createElement('a');
        a_tag_third.href = url_third;
        a_tag_third.rel = "noopener";
        a_tag_third.target = "_blank";
        // set styles
        a_tag_third.style.width = "32%";
        a_tag_third.style.height = "fit-content";
        a_tag_third.style.color = "white";
        a_tag_third.style.fontFamily = "JetBrains Mono";
        const main = shell.currentWidget;
        if (main instanceof _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget) {
            const widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget();
            if (main.contentHeader.node.hasChildNodes()) {
                const childNum = main.contentHeader.node.childElementCount;
                for (var i = 0; i < childNum; i++) {
                    (_a = main.contentHeader.node.firstChild) === null || _a === void 0 ? void 0 : _a.remove();
                }
            }
            // background-color
            // Set color
            main.contentHeader.node.style.backgroundColor = "rgb(102, 102, 102)";
            main.contentHeader.node.style.color = "white";
            // Set size
            main.contentHeader.node.style.width = "fit-content";
            main.contentHeader.node.style.height = "fit-content";
            // Set position
            main.contentHeader.node.style.zIndex = "10";
            main.contentHeader.node.style.position = "absolute";
            main.contentHeader.node.style.removeProperty("top");
            main.contentHeader.node.style.bottom = "0px";
            main.contentHeader.node.style.left = "0px";
            main.contentHeader.node.style.paddingTop = "5px";
            main.contentHeader.node.style.paddingLeft = "87px";
            main.contentHeader.node.style.paddingRight = "15px";
            main.contentHeader.node.style.display = "flex";
            main.contentHeader.node.style.justifyContent = "space-between";
            main.contentHeader.node.style.alignItems = "center";
            main.contentHeader.node.appendChild(a_tag_first);
            (_b = main.contentHeader.node.firstChild) === null || _b === void 0 ? void 0 : _b.appendChild(img_tag_first);
            main.contentHeader.node.appendChild(a_tag_second);
            (_c = main.contentHeader.node.lastChild) === null || _c === void 0 ? void 0 : _c.appendChild(img_tag_second);
            main.contentHeader.node.appendChild(a_tag_third);
            (_d = main.contentHeader.node.lastChild) === null || _d === void 0 ? void 0 : _d.appendChild(img_tag_third);
            main.contentHeader.node.click();
            return widget;
        }
        else {
            console.log('no contentheader');
        }
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/config/config.json":
/*!********************************!*\
  !*** ./lib/config/config.json ***!
  \********************************/
/***/ ((module) => {

module.exports = JSON.parse('{"api_root_url":"https://geek10-api-gyfmmv6njq-an.a.run.app/","api_reccomend":"/recommend/"}');

/***/ }),

/***/ "./lib/config/user_config.json":
/*!*************************************!*\
  !*** ./lib/config/user_config.json ***!
  \*************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"user_id":"00000","programming_learning_level":1,"python_learning_level":1,"nlp_theory_level":1,"nlp_skill_level":1,"ip_theory_level":1,"ip_skill_level":1,"sp_theory_level":1,"sp_skill_level":1,"ml_theory_level":1,"ml_skill_level":1,"db_theory_level":1,"db_skill_level":1,"atcoder_rate":1,"english_reading_level":1,"english_resistance_level":2,"translation_resistance":1,"learning_directivity":1}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.5ce85bb3b94a183fdc61.js.map