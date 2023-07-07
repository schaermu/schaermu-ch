describe('home page', () => {
    it('has correct titles', () => {
        cy.visit('/');

        cy.title().should('eq', 'der begrüssende schärmu');
        cy.get('h1').should('contain.text', 'Willkommen!');
    });

    it('contains 2 cards linking to blog and cv', () => {
        cy.visit('/');

        cy.get('article').should('have.length', 2);
        cy.get('article').each(($el) => {
            cy.wrap($el).get('a').should('exist');
            cy.wrap($el).get('a').should('have.attr', 'href');
        })
    });
})
