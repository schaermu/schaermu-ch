// aligns width of an element to its toggle root when on mobile
const updateMobileWidth = ($element: Element) => {
    const $toggleRoot = $element.closest('[data-toggle-root]');
    if (!$toggleRoot) return;
    if (window.matchMedia("(max-width: 767px)").matches) {
        $element.setAttribute(
            "style",
            `width: ${window.getComputedStyle($toggleRoot).getPropertyValue("width")}`,
        );
    }
};

// bind all toggle buttons, store targets
const toggleTargets: Element[] = [];
const buttons = document.querySelectorAll('[data-toggle-target]');
buttons.forEach(($button) => {
    const target = ($button as HTMLElement).dataset.toggleTarget;
    const $target = document.querySelector(target ?? '');
    if (!$target) return;
    toggleTargets.push($target);

    // bind show event
    $button.addEventListener("click", (e) => {
        $target.classList.remove("hidden");
        updateMobileWidth($target);
    });

    // bind close event
    $target.querySelector('[data-toggle-closer]')?.addEventListener("click", (event) => {
        $target.classList.add("hidden");
    });
})

// on window resize, we also resize all toggle targets
window.addEventListener("resize", () => {
    toggleTargets.forEach((target) => {
        updateMobileWidth(target);
    });
});

const closeAllTargets = () => {
    toggleTargets.forEach(($target) => {
        $target.classList.add("hidden");
    });
}

// close all targets when click occurs outside a target
const targetIds = toggleTargets.map((target) => target.id);
window.addEventListener("click", (e) => {
    let $target = e.target as HTMLElement,
        insideMenu = false;

    while ($target.parentElement && !insideMenu) {
        if ($target.dataset?.toggleTarget) return true;
        targetIds.forEach((id) => {
            const $toggleTarget = $target.closest(`#${id}`);
            if ($toggleTarget) {
                insideMenu = true;
                return;
            }
        })
        $target = $target.parentElement;
    }
    if (!insideMenu) {
        closeAllTargets();
    }
});