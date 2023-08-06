# MMI Technical Architecture

## Browser extension

![MMI Technical Architecture](./assets/images/technical-architecture.png)

With the browser extension, users interact with dapps (web pages) which generate transaction parameters for interacting with smart contracts.

The browser extension passes these parameters to the custodian API, where they are brought to the attention of approvers, who may approve or reject them.

The custodian signs and submits the transaction, and watches for it to be confirmed (mined or validated).

The custodian then triggers webhooks in MMI's backend, which informs the browser extension through a websocket stream.