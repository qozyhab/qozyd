import Popper from "popper.js"


export default{
  bind: function (el, binding, vnode) {
    el.addEventListener('click', () => {
      let popout = vnode.context.$refs[binding.value]

      if (!el.$popper) {
        el.$popper = new Popper(el, popout, {
            placement: binding.arg ? binding.arg : "bottom"
        })
      }

      popout.style.display = popout.style.display === "block" ? "none" : "block"
    })
  },
  unbind: function (el) {
    if (el.$popper) {
      el.$popper.destroy()
    }
  },
}

