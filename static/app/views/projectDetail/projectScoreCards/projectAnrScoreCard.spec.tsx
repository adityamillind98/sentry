import {render, screen, waitFor} from 'sentry-test/reactTestingLibrary';

import {PageFilters} from 'sentry/types';
import {ProjectAnrScoreCard} from 'sentry/views/projectDetail/projectScoreCards/projectAnrScoreCard';

describe('ProjectDetail > ProjectAnr', function () {
  let endpointMock, endpointMockPreviousPeriod;

  const organization = TestStubs.Organization();

  const selection = {
    projects: [1],
    environments: [],
    datetime: {
      period: '7d',
      start: null,
      end: null,
      utc: false,
    },
  } as PageFilters;

  beforeEach(function () {
    endpointMock = MockApiClient.addMockResponse({
      url: `/organizations/${organization.slug}/sessions/`,
      match: [MockApiClient.matchQuery({statsPeriod: '7d'})],
      body: {
        groups: [
          {
            by: {},
            totals: {
              'foreground_anr_rate()': 0.11561866125760649,
            },
          },
        ],
      },
      status: 200,
    });

    endpointMockPreviousPeriod = MockApiClient.addMockResponse({
      url: `/organizations/${organization.slug}/sessions/`,
      match: [MockApiClient.matchQuery({start: '2017-10-03T02:41:20.000'})], // setup mocks a constant current date, so this works
      body: {
        groups: [
          {
            by: {},
            totals: {
              'foreground_anr_rate()': 0.08558558558558559,
            },
          },
        ],
      },
      status: 200,
    });
  });

  afterEach(function () {
    MockApiClient.clearMockResponses();
  });

  it('calls api with anr rate', async function () {
    render(
      <ProjectAnrScoreCard
        organization={{...organization}}
        selection={selection}
        isProjectStabilized
        query="release:abc"
      />
    );

    expect(endpointMock).toHaveBeenCalledWith(
      `/organizations/${organization.slug}/sessions/`,
      expect.objectContaining({
        query: {
          environment: [],
          field: ['foreground_anr_rate()'],
          includeSeries: '0',
          includeTotals: '1',
          interval: '1h',
          project: [1],
          query: 'release:abc',
          statsPeriod: '7d',
        },
      })
    );

    expect(endpointMockPreviousPeriod).toHaveBeenCalledWith(
      `/organizations/${organization.slug}/sessions/`,
      expect.objectContaining({
        query: {
          end: '2017-10-10T02:41:20.000',
          environment: [],
          field: ['foreground_anr_rate()'],
          includeSeries: '0',
          includeTotals: '1',
          interval: '1h',
          project: [1],
          query: 'release:abc',
          start: '2017-10-03T02:41:20.000',
        },
      })
    );

    await waitFor(() => expect(screen.getByText('11.562%')).toBeInTheDocument());
    await waitFor(() => expect(screen.getByText('0.03%')).toBeInTheDocument());
  });
});