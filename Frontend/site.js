document.addEventListener('DOMContentLoaded', function () {
  const loader = document.getElementById('page-loader');
  if (loader) {
    setTimeout(() => loader.classList.add('hidden'), 300);
  }

  const stepper = document.getElementById('page-stepper');
  if (stepper) {
    const steps = [
      { step: 1, label: 'Profile', href: 'user.html' },
      { step: 2, label: 'Upload', href: 'upload.html' },
      { step: 3, label: 'Files', href: 'selectfiles.html' },
      { step: 4, label: 'Report', href: 'qualityreport.html' }
    ];

    const raw = (location.pathname || '').split('/').pop() || 'Home.html';
    const current = raw.split('?')[0].split('#')[0];
    const currentLower = current.toLowerCase();
    const activeIndex = steps.findIndex(({ href }) => {
      const hrefLower = href.toLowerCase();
      return hrefLower === currentLower || hrefLower.endsWith('/' + currentLower) || hrefLower.endsWith(currentLower);
    });

    stepper.innerHTML = '';

    steps.forEach(({ step, label }, index) => {
      if (index > 0) {
        const connector = document.createElement('div');
        connector.className = 'step-connector';
        connector.setAttribute('aria-hidden', 'true');

        if (index < activeIndex) {
          connector.classList.add('completed');
        }

        stepper.appendChild(connector);
      }

      const item = document.createElement('button');
      item.type = 'button';
      item.className = 'step';
      item.setAttribute('data-step', String(step));
      item.setAttribute('disabled', 'disabled');
      item.setAttribute('aria-disabled', 'true');
      item.setAttribute('tabindex', '-1');
      item.innerHTML = `
        <span class="step-index">${step}</span>
        <span class="step-label">${label}</span>
      `;

      if (index < activeIndex) {
        item.classList.add('completed');
      }

      if (index === activeIndex) {
        item.classList.add('active');
      }

      stepper.appendChild(item);
    });

    const completedSteps = stepper.querySelectorAll('.step.completed').length;
    const totalSteps = steps.length;
    const progressWidth = totalSteps > 1 ? (completedSteps / (totalSteps - 1)) * 100 : 0;
    stepper.style.setProperty('--progress-width', `${Math.max(Math.min(progressWidth, 100), 0)}%`);
  }
});

window.SiteUI = {
  showLoader: () => {
    const el = document.getElementById('page-loader');
    if (el) el.classList.remove('hidden');
  },
  hideLoader: () => {
    const el = document.getElementById('page-loader');
    if (el) el.classList.add('hidden');
  },
};
