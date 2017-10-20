import { AideFePage } from './app.po';

describe('aide-fe App', () => {
  let page: AideFePage;

  beforeEach(() => {
    page = new AideFePage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
