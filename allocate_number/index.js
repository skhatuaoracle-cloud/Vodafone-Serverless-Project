exports.handler = async (event) => {

    console.log("Received Event:", JSON.stringify(event));

    const prefixes = [
        "98765",
        "98654",
        "98989",
        "98888"
    ];

    const prefix =
        prefixes[Math.floor(Math.random() * prefixes.length)];

    const number =
        prefix +
        Math.floor(10000 + Math.random() * 90000);

    event.mobileNumber = number;

    event.connectionStatus = "ALLOCATED";

    return event;
};