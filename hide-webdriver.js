const defaultGetter = Object.getOwnPropertyDescriptor(Navigator.prototype, 'webdriver').get;
defaultGetter.apply(navigator); // true
defaultGetter.toString(); // "function get webdriver() { [native code] }"
Object.defineProperty(Navigator.prototype, 'webdriver', {
  set: undefined,
  enumerable: true,
  configurable: true,
  get: new Proxy(defaultGetter, { apply: (target, thisArg, args) => {
    // emulate getter call validation
    Reflect.apply(target, thisArg, args);
    return false;
  }})
});
const patchedGetter = Object.getOwnPropertyDescriptor(Navigator.prototype, 'webdriver').get;
patchedGetter.apply(navigator); // false
patchedGetter.toString(); // "function () { [native code] }"