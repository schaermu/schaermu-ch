it('titles are correct', () => {
    cy.visit('/');

    cy.title().should('eq', 'der bloggende schärmu');
    cy.get('h1').should('contain.text', 'Willkommen!');
});