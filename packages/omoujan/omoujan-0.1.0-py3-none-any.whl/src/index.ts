import axios from 'axios';
import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin,
} from '@jupyterlab/application';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { NotebookActions } from "@jupyterlab/notebook";
import { Widget } from '@lumino/widgets';

import config from './config/config.json'
import user_config from './config/user_config.json'

const API_URL: string = config["api_root_url"] + config["api_reccomend"]

const extension: JupyterFrontEndPlugin<void> = {
    id: 'creative',
    autoStart: true,
    optional: [],
    requires: [],
    activate,
};

interface InsideData {
    "url": string,
    "title": string,
    "img_base64": any
}

interface ResponseData {
    result: InsideData[];
}

function activate(
    app: JupyterFrontEnd,
): void {
    const { shell } = app;

    // Call function after finish executing cell
    NotebookActions.executed.connect((_, action) => {
        console.log("action: ", action)
        if (action.success) {
            console.log("action.success", action.success)
        } else {
            console.log("action.success", action.success)
            console.log("action.error", action.error)
            let headers = {
                "accept": "application/json",
                "Content-Type": "application/json"
            }
            console.log("user_config: ", user_config)
            console.log("config: ", config)

            let request_data: { [name: string]: any } = user_config
            request_data['code_text'] = 'string'
            request_data['output_text'] = ''
            request_data['error_text'] = String(action.error)

            console.log("request_data: ", request_data)
            // Post data
            axios.post(API_URL, request_data, { headers: headers }).then(
                ({ data }) => {
                    console.log("data: ", data)
                    // const widget = createWidget(data)
                    createWidget(data)
                    // console.log('widget: ', widget)
                }
            );
        }
    })

    function createWidget(data: ResponseData) {
        let url_first: string = data.result[0].url
        let img_first: BinaryType = data.result[0].img_base64
        let url_second: string = data.result[1].url
        let img_second: BinaryType = data.result[1].img_base64
        let url_third: string = data.result[2].url
        let img_third: BinaryType = data.result[2].img_base64

        //
        let img_tag_first = document.createElement('img')
        img_tag_first.src = "data:image/gif;base64," + img_first
        img_tag_first.style.width = "100%"
        // set elems
        let a_tag_first = document.createElement('a');
        a_tag_first.href = url_first
        a_tag_first.rel = "noopener"
        a_tag_first.target = "_blank"
        // set styles
        a_tag_first.style.width = "32%"
        a_tag_first.style.height = "fit-content"
        a_tag_first.style.color = "white"
        a_tag_first.style.fontFamily = "JetBrains Mono"

        let img_tag_second = document.createElement('img')
        img_tag_second.src = "data:image/gif;base64," + img_second
        img_tag_second.style.width = "100%"
        let a_tag_second = document.createElement('a');
        a_tag_second.href = url_second
        a_tag_second.rel = "noopener"
        a_tag_second.target = "_blank"
        // set styles
        a_tag_second.style.width = "32%"
        a_tag_second.style.height = "fit-content"
        a_tag_second.style.color = "white"
        a_tag_second.style.fontFamily = "JetBrains Mono"

        let img_tag_third = document.createElement('img')
        img_tag_third.src = "data:image/gif;base64," + img_third
        img_tag_third.style.width = "100%"
        let a_tag_third = document.createElement('a');
        a_tag_third.href = url_third
        a_tag_third.rel = "noopener"
        a_tag_third.target = "_blank"
        // set styles
        a_tag_third.style.width = "32%"
        a_tag_third.style.height = "fit-content"
        a_tag_third.style.color = "white"
        a_tag_third.style.fontFamily = "JetBrains Mono"

        const main = shell.currentWidget;
        if (main instanceof MainAreaWidget) {
            const widget = new Widget();

            if (main.contentHeader.node.hasChildNodes()) {
                const childNum: number = main.contentHeader.node.childElementCount
                for (var i = 0; i < childNum; i++) {
                    main.contentHeader.node.firstChild?.remove();
                }
            }

            // background-color

            // Set color
            main.contentHeader.node.style.backgroundColor = "rgb(102, 102, 102)"
            main.contentHeader.node.style.color = "white"
            // Set size
            main.contentHeader.node.style.width = "fit-content"
            main.contentHeader.node.style.height = "fit-content"
            // Set position
            main.contentHeader.node.style.zIndex = "10"
            main.contentHeader.node.style.position = "absolute"
            main.contentHeader.node.style.removeProperty("top")
            main.contentHeader.node.style.bottom = "0px"
            main.contentHeader.node.style.left = "0px"

            main.contentHeader.node.style.paddingTop = "5px"
            main.contentHeader.node.style.paddingLeft = "87px"
            main.contentHeader.node.style.paddingRight = "15px"
            main.contentHeader.node.style.display = "flex"
            main.contentHeader.node.style.justifyContent = "space-between"
            main.contentHeader.node.style.alignItems = "center"


            main.contentHeader.node.appendChild(a_tag_first)
            main.contentHeader.node.firstChild?.appendChild(img_tag_first)
            main.contentHeader.node.appendChild(a_tag_second)
            main.contentHeader.node.lastChild?.appendChild(img_tag_second)

            main.contentHeader.node.appendChild(a_tag_third)
            main.contentHeader.node.lastChild?.appendChild(img_tag_third)
            main.contentHeader.node.click()

            return widget;
        } else {
            console.log('no contentheader')
        }
    }
}

export default extension;
