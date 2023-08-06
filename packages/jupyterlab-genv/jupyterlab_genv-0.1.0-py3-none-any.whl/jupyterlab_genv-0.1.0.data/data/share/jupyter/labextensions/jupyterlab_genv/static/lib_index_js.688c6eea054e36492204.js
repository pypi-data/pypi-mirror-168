"use strict";
(self["webpackChunkjupyterlab_genv"] = self["webpackChunkjupyterlab_genv"] || []).push([["lib_index_js"],{

/***/ "./lib/dialogs.js":
/*!************************!*\
  !*** ./lib/dialogs.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Dialogs": () => (/* binding */ Dialogs)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);


var Dialogs;
(function (Dialogs) {
    async function noKernel() {
        const { button } = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
            title: 'No Kernel',
            body: 'You need a kernel in order to run in a GPU environment.',
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: 'Later' }),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.warnButton({ label: 'Select kernel', accept: true })
            ]
        });
        return button.accept;
    }
    Dialogs.noKernel = noKernel;
    async function notSupportedKernel() {
        const { button } = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
            title: 'Not a genv Kernel',
            body: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
                "Please select a genv kernel.",
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
                "If you don't have any, run the following command:",
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("code", null, "python -m jupyterlab_genv install"))),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: 'Later' }),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.warnButton({ label: 'Select kernel', accept: true })
            ]
        });
        return button.accept;
    }
    Dialogs.notSupportedKernel = notSupportedKernel;
    async function activate(envs, kernel_id) {
        const placeholder = 'Create a new environment';
        let { value } = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getItem({
            title: 'Activate GPU Environment',
            items: [placeholder, ...envs.map(env => env.eid)],
            okLabel: 'Next'
        });
        if (value === placeholder) {
            value = kernel_id;
        }
        return value;
    }
    Dialogs.activate = activate;
    async function configure(eid) {
        const { button } = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
            title: 'Configure GPU Environment',
            body: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
                "Open a terminal and run the following command:",
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("code", null,
                    "genv activate --id ",
                    eid),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
                "Then, configure the environment with normal genv commands.",
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
                "If you are not familiar with how to configure genv environments, check out the genv reference.",
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
                "You can find it at https://github.com/run-ai/genv.",
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("b", null, "IMPORTANT"),
                "You will need to restart the kernel for changes form the terminal to effect.")),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: 'Later' }),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Open a terminal' })
            ]
        });
        return button.accept;
    }
    Dialogs.configure = configure;
})(Dialogs || (Dialogs = {}));


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Handler": () => (/* binding */ Handler)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-genv', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}
var Handler;
(function (Handler) {
    async function activate(kernel_id, eid) {
        const body = JSON.stringify({
            eid: eid,
            kernel_id: kernel_id
        });
        await requestAPI('activate', {
            body: body,
            method: 'POST'
        });
    }
    Handler.activate = activate;
    async function devices() {
        return await requestAPI('devices');
    }
    Handler.devices = devices;
    async function envs() {
        return await requestAPI('envs');
    }
    Handler.envs = envs;
    async function find(kernel_id) {
        return (await requestAPI(`find?kernel_id=${kernel_id}`)) || null;
    }
    Handler.find = find;
})(Handler || (Handler = {}));


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ButtonExtension": () => (/* binding */ ButtonExtension),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _dialogs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./dialogs */ "./lib/dialogs.js");





async function openTerminal(eid, app) {
    // NOTE(raz): the terminal is returned only when it's created in the first time.
    //    this means that we can't send commands to the terminal if it's already running.
    //    we should consider either creating a terminal per kernel or fixing this.
    //    we tried opening a terminal per kernel but it seems like terminal names can't
    //    be long enough to contain a kernel identifier.
    //    here's a reference:
    //    https://github.com/jupyterlab/jupyterlab/blob/v3.4.7/packages/terminal-extension/src/index.ts#L323
    const terminal = await app.commands.execute('terminal:open', { name: 'genv' });
    if (terminal) {
        app.shell.add(terminal, 'main', { mode: 'split-bottom' });
        terminal.content.session.send({
            type: 'stdin',
            content: [
                [
                    '# this is a terminal for configuring your genv environment.',
                    '# it will be activated in your environment.',
                    '# you can configure your environment and attach devices from here.',
                    '# ',
                    '# you can start with running the following command:',
                    '# ',
                    '#     genv attach --help',
                    '# ',
                    '# for more information check out the reference at https://github.com/run-ai/genv',
                    '# ',
                    '# IMPORTANT: you will need to restart your Jupyter kernel after configuring the environment from the terminal.',
                    '',
                    `genv activate --id ${eid}`
                ]
                    .map(line => line + '\n')
                    .join('')
            ]
        });
    }
}
async function handleClick(kernel, app) {
    if (kernel) {
        const spec = await kernel.spec;
        if (spec === null || spec === void 0 ? void 0 : spec.name.endsWith('-genv')) {
            let eid = await _handler__WEBPACK_IMPORTED_MODULE_3__.Handler.find(kernel.id);
            if (!eid) {
                const envs = await _handler__WEBPACK_IMPORTED_MODULE_3__.Handler.envs();
                eid = await _dialogs__WEBPACK_IMPORTED_MODULE_4__.Dialogs.activate(envs, kernel.id);
                if (eid) {
                    await _handler__WEBPACK_IMPORTED_MODULE_3__.Handler.activate(kernel.id, eid);
                }
            }
            if (eid) {
                if (await _dialogs__WEBPACK_IMPORTED_MODULE_4__.Dialogs.configure(eid)) {
                    await openTerminal(eid, app);
                }
            }
        }
        else {
            if (await _dialogs__WEBPACK_IMPORTED_MODULE_4__.Dialogs.notSupportedKernel()) {
                await app.commands.execute('notebook:change-kernel');
            }
        }
    }
    else {
        if (await _dialogs__WEBPACK_IMPORTED_MODULE_4__.Dialogs.noKernel()) {
            await app.commands.execute('notebook:change-kernel');
        }
    }
}
class ButtonExtension {
    constructor(app) {
        this._app = app;
    }
    createNew(panel, _context) {
        // Create the toolbar button
        const mybutton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            label: 'GPUs',
            tooltip: 'Configure the GPU environment',
            onClick: async () => {
                var _a;
                await handleClick((_a = panel.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel, this._app);
            }
        });
        // Add the toolbar button to the notebook toolbar
        panel.toolbar.insertItem(10, 'mybutton', mybutton);
        // The ToolbarButton class implements `IDisposable`, so the
        // button *is* the extension for the purposes of this method.
        return mybutton;
    }
}
class DevicesWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    constructor(devices) {
        super();
        // this.addClass('my-apodWidget');
        this.div = document.createElement('div');
        this.node.appendChild(this.div);
    }
}
const plugin = {
    id: 'jupyterlab_genv:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    activate: async (app, palette) => {
        app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension(app));
        const devicesInfos = await _handler__WEBPACK_IMPORTED_MODULE_3__.Handler.devices();
        const devicesWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({
            content: new DevicesWidget(devicesInfos)
            // content: ReactWidget.create(
            //   <>
            //     {devicesInfos.map((device: { eid: string }, i: number) => (
            //       <div>
            //         GPU {i}:{' '}
            //         {device.eid === '' ? (
            //           <span style={{ color: 'green' }}>available</span>
            //         ) : (
            //           <span>used by enviornment {device.eid}</span>
            //         )}
            //       </div>
            //     ))}
            //   </>
            // )
        });
        devicesWidget.id = 'jupyterlab_genv.devices';
        devicesWidget.title.label = 'GPUs: Devices';
        devicesWidget.title.closable = true;
        // https://jupyterlab.readthedocs.io/en/stable/extension/extension_tutorial.html#show-a-new-image-on-demand
        // https://github.com/jupyterlab/extension-examples/blob/master/react-widget/src/widget.tsx
        // devicesWidget.toolbar.insertItem(
        //   0,
        //   'refresh',
        //   new ToolbarButton({ label: 'Refresh' })
        // );
        const devicesCommand = 'jupyterlab_genv.devices.open';
        app.commands.addCommand(devicesCommand, {
            label: 'GPUs: Show Devices',
            execute: () => {
                if (!devicesWidget.isAttached) {
                    app.shell.add(devicesWidget, 'main');
                }
                app.shell.activateById(devicesWidget.id);
            }
        });
        palette.addItem({ command: devicesCommand, category: 'GPUs' });
        const envsInfos = await _handler__WEBPACK_IMPORTED_MODULE_3__.Handler.envs();
        const envsWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({
            content: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_2___default().createElement((react__WEBPACK_IMPORTED_MODULE_2___default().Fragment), null, envsInfos.map((env) => (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null,
                `${env['eid']} ${env['user']}`,
                env['name'] !== '' ? ` ${env['name']}` : null)))))
        });
        envsWidget.id = 'jupyterlab_genv.envs';
        envsWidget.title.label = 'GPUs: Environments';
        envsWidget.title.closable = true;
        // https://jupyterlab.readthedocs.io/en/stable/extension/extension_tutorial.html#show-a-new-image-on-demand
        // https://github.com/jupyterlab/extension-examples/blob/master/react-widget/src/widget.tsx
        // envsWidget.toolbar.insertItem(
        //   0,
        //   'refresh',
        //   new ToolbarButton({ label: 'Refresh' })
        // );
        const envsCommand = 'jupyterlab_genv.envs.open';
        app.commands.addCommand(envsCommand, {
            label: 'GPUs: Show Environments',
            execute: () => {
                if (!envsWidget.isAttached) {
                    app.shell.add(envsWidget, 'main');
                }
                app.shell.activateById(envsWidget.id);
            }
        });
        palette.addItem({ command: envsCommand, category: 'GPUs' });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.688c6eea054e36492204.js.map