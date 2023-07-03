it('titles are correct', () => {
    cy.visit('/');

    cy.title().should('eq', 'the writings and musings of schaermu.');
    cy.get('h1').should('have.text', 'Welcome!');
});