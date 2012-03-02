// Add filter property to Array if it doesn't exist.
if (!Array.prototype.filter) {
  Array.prototype.filter = function(fun /*, thisp */) {
    "use strict";

    if (this == null)
      throw new TypeError();

    var t = Object(this);
    var len = t.length >>> 0;
    if (typeof fun != "function")
      throw new TypeError();

    var res = [];
    var thisp = arguments[1];
    for (var i = 0; i < len; i++) {
      if (i in t) {
        var val = t[i]; // in case fun mutates this
        if (fun.call(thisp, val, i, t))
          res.push(val);
      }
    }
    return res;
  };
}

// Patch buggy filtering functionality.
TWTR.Widget.prototype._sortByMagic = function (tweets) {
  if (this._tweetFilter) {
    tweets = tweets.filter(this._tweetFilter);
  }
  switch (this._behavior) {
    case "all":
      this._sortByLatest(tweets);
      break;
    case "preloaded":
      default:
      this._sortByDefault(tweets);
      break;
  }
  if (this._isLive && this._behavior !== "all") {
    this.intervalJob.set(this.results);
    this.intervalJob.start();
  }
  return this;
};
