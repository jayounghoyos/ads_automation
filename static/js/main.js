// main.js

const selectedVacancies = [];

function addVacancy() {
    const input = document.getElementById('vacancyInput');
    const inputValues = input.value.trim();

    if (!inputValues) {
        alert('Por favor, ingresa uno o más IDs de vacantes.');
        return;
    }

    // Separar los IDs por comas y eliminar espacios
    const vacancyIds = inputValues.split(',').map(id => id.trim());

    // Validar cada ID individualmente
    vacancyIds.forEach(vacancyId => {
        if (isNaN(vacancyId) || parseInt(vacancyId) <= 0) {
            alert(`El ID "${vacancyId}" no es un número positivo válido.`);
            return;
        }

        if (selectedVacancies.some(v => v.id === vacancyId)) {
            alert(`La vacante con ID "${vacancyId}" ya ha sido agregada.`);
            return;
        }

        if (!jobData[vacancyId]) {
            alert(`El ID "${vacancyId}" no es válido. Intenta con otro ID.`);
            return;
        }

        const jobTitle = jobData[vacancyId];
        selectedVacancies.push({ id: vacancyId, title: jobTitle });
    });

    renderVacancyList();
    input.value = '';
}


function renderVacancyList() {
    const list = document.getElementById('vacancyList');
    list.innerHTML = '';

    selectedVacancies.forEach((vacancy, index) => {
        const li = document.createElement('li');
        li.innerHTML = `Vacante ID: ${vacancy.id} <br> Job Title: ${vacancy.title}`;

        const removeButton = document.createElement('button');
        removeButton.textContent = 'Eliminar';
        removeButton.onclick = () => {
            selectedVacancies.splice(index, 1);
            renderVacancyList();
        };

        li.appendChild(removeButton);
        list.appendChild(li);
    });
}

function automatizar() {
    if (selectedVacancies.length === 0) {
        alert('No hay vacantes seleccionadas para automatizar.');
        return;
    }
    alert(`Automatizando la publicación de ${selectedVacancies.length} vacante(s)`);
}
