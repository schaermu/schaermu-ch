export default function nl2br(str: string, isXhtml: boolean = true) {
    var breakTag = isXhtml ? "<br />" : "<br>";
    return (str + "").replace(
        /([^>\r\n]?)(\r\n|\n\r|\r|\n)/g,
        "$1" + breakTag + "$2",
    );
}