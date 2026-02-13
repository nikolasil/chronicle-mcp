window.BENCHMARK_DATA = {
  "lastUpdate": 1771007680228,
  "repoUrl": "https://github.com/nikolasil/chronicle-mcp",
  "entries": {
    "Python Benchmark": [
      {
        "commit": {
          "author": {
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "id": "89344ee2dc736c40cce36a49be24274bc9122b6d",
          "message": "Refactor/service layer",
          "timestamp": "2026-02-12T22:16:20Z",
          "url": "https://github.com/nikolasil/chronicle-mcp/pull/7/commits/89344ee2dc736c40cce36a49be24274bc9122b6d"
        },
        "date": 1771007450064,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 202997.33120407932,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017560946983814427",
            "extra": "mean: 4.926173137688544 usec\nrounds: 16149"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 206040.18947180183,
            "unit": "iter/sec",
            "range": "stddev: 7.525074787073789e-7",
            "extra": "mean: 4.853422055976403 usec\nrounds: 35827"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 202891.97657641274,
            "unit": "iter/sec",
            "range": "stddev: 7.617671230165135e-7",
            "extra": "mean: 4.92873112517282 usec\nrounds: 36954"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 298405.47058101237,
            "unit": "iter/sec",
            "range": "stddev: 7.246965013582401e-7",
            "extra": "mean: 3.3511449976199943 usec\nrounds: 41780"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 435752.2957642214,
            "unit": "iter/sec",
            "range": "stddev: 5.757586083173463e-7",
            "extra": "mean: 2.2948817704934914 usec\nrounds: 97666"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 449418.9154257366,
            "unit": "iter/sec",
            "range": "stddev: 5.482903688907929e-7",
            "extra": "mean: 2.225095485918067 usec\nrounds: 92422"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5819617.026295126,
            "unit": "iter/sec",
            "range": "stddev: 2.2007055255821924e-8",
            "extra": "mean: 171.83261295065682 nsec\nrounds: 193462"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52629.937139457485,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020232195644447022",
            "extra": "mean: 19.00059271114509 usec\nrounds: 13747"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 88742.52386070734,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013202850647986294",
            "extra": "mean: 11.268554876460657 usec\nrounds: 38614"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20702.7881894456,
            "unit": "iter/sec",
            "range": "stddev: 0.000005408257895010322",
            "extra": "mean: 48.302672608600886 usec\nrounds: 7349"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43765.25823914715,
            "unit": "iter/sec",
            "range": "stddev: 0.000002736394966006844",
            "extra": "mean: 22.84917398489197 usec\nrounds: 16944"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9182.772533066312,
            "unit": "iter/sec",
            "range": "stddev: 0.000004945935025387477",
            "extra": "mean: 108.89957214981561 usec\nrounds: 4754"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4466.392076703203,
            "unit": "iter/sec",
            "range": "stddev: 0.00006599150311584468",
            "extra": "mean: 223.89436100247926 usec\nrounds: 1795"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19525.21652020451,
            "unit": "iter/sec",
            "range": "stddev: 0.000005236560496958765",
            "extra": "mean: 51.21582129269651 usec\nrounds: 9731"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1894258.5681440348,
            "unit": "iter/sec",
            "range": "stddev: 8.193633336638417e-8",
            "extra": "mean: 527.9110343313853 nsec\nrounds: 183790"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244322.00202718773,
            "unit": "iter/sec",
            "range": "stddev: 7.919792571198925e-7",
            "extra": "mean: 4.0929592574667994 usec\nrounds: 30165"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1752441.5922098642,
            "unit": "iter/sec",
            "range": "stddev: 5.640844953347712e-8",
            "extra": "mean: 570.6324276059266 nsec\nrounds: 69171"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1280927.4725196338,
            "unit": "iter/sec",
            "range": "stddev: 1.1642029932570624e-7",
            "extra": "mean: 780.6843255792944 nsec\nrounds: 156446"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285534.43603118,
            "unit": "iter/sec",
            "range": "stddev: 6.425512446051044e-7",
            "extra": "mean: 3.5022045463223956 usec\nrounds: 53494"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148176.23770617234,
            "unit": "iter/sec",
            "range": "stddev: 9.809295161225622e-7",
            "extra": "mean: 6.748720412128163 usec\nrounds: 23971"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64302.6170520847,
            "unit": "iter/sec",
            "range": "stddev: 0.00040582778902836287",
            "extra": "mean: 15.551466578568746 usec\nrounds: 23458"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7970209.8373584775,
            "unit": "iter/sec",
            "range": "stddev: 1.0913893488205951e-8",
            "extra": "mean: 125.46721107805598 nsec\nrounds: 77919"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4cbb0b8538ecab84619aa23bdb3c8494121c84e4",
          "message": "Merge pull request #7 from nikolasil/refactor/service-layer\n\nRefactor/service layer",
          "timestamp": "2026-02-13T13:33:08-05:00",
          "tree_id": "2a3e9dbd387d8c855be01f4b1ac87a35836b4fc0",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/4cbb0b8538ecab84619aa23bdb3c8494121c84e4"
        },
        "date": 1771007679329,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 200808.2875622288,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019048679059906653",
            "extra": "mean: 4.979874148322232 usec\nrounds: 13063"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 207330.1396613699,
            "unit": "iter/sec",
            "range": "stddev: 7.505177733293075e-7",
            "extra": "mean: 4.823225420256261 usec\nrounds: 37836"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 200241.04425699532,
            "unit": "iter/sec",
            "range": "stddev: 8.12884800413658e-7",
            "extra": "mean: 4.993981147624112 usec\nrounds: 36388"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 310389.9271689967,
            "unit": "iter/sec",
            "range": "stddev: 7.405135768448365e-7",
            "extra": "mean: 3.221754034097679 usec\nrounds: 43876"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 440011.87176501437,
            "unit": "iter/sec",
            "range": "stddev: 5.640474272792331e-7",
            "extra": "mean: 2.2726659532814693 usec\nrounds: 100929"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 446610.9077901452,
            "unit": "iter/sec",
            "range": "stddev: 5.281128473963275e-7",
            "extra": "mean: 2.2390854825916677 usec\nrounds: 101740"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5631880.271195269,
            "unit": "iter/sec",
            "range": "stddev: 2.3056617217610387e-8",
            "extra": "mean: 177.5605928830627 nsec\nrounds: 199204"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52373.75076291122,
            "unit": "iter/sec",
            "range": "stddev: 0.000002008855059472649",
            "extra": "mean: 19.093534173766987 usec\nrounds: 13168"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 90209.09779784486,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013583795135008357",
            "extra": "mean: 11.085356404305935 usec\nrounds: 37623"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20585.567556744838,
            "unit": "iter/sec",
            "range": "stddev: 0.000004875017544676315",
            "extra": "mean: 48.577723069498326 usec\nrounds: 6164"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43493.46189266131,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027291263616138",
            "extra": "mean: 22.991961469241673 usec\nrounds: 17233"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9178.825476446713,
            "unit": "iter/sec",
            "range": "stddev: 0.000005434594459993481",
            "extra": "mean: 108.94640088386535 usec\nrounds: 4752"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4508.173256441382,
            "unit": "iter/sec",
            "range": "stddev: 0.00006537266338557622",
            "extra": "mean: 221.81933637336962 usec\nrounds: 1864"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19672.74710999772,
            "unit": "iter/sec",
            "range": "stddev: 0.0000052376695319537485",
            "extra": "mean: 50.83174171907078 usec\nrounds: 9540"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1944753.7912538168,
            "unit": "iter/sec",
            "range": "stddev: 8.032113317932895e-8",
            "extra": "mean: 514.2039082259778 nsec\nrounds: 169751"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244731.40820410478,
            "unit": "iter/sec",
            "range": "stddev: 8.287741823724674e-7",
            "extra": "mean: 4.086112229477325 usec\nrounds: 33182"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1762648.7385354755,
            "unit": "iter/sec",
            "range": "stddev: 5.44141491824896e-8",
            "extra": "mean: 567.3280093405649 nsec\nrounds: 67440"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1292812.3294619953,
            "unit": "iter/sec",
            "range": "stddev: 1.3232814608585377e-7",
            "extra": "mean: 773.5074745273631 nsec\nrounds: 151470"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 284487.41700296977,
            "unit": "iter/sec",
            "range": "stddev: 6.924620226701099e-7",
            "extra": "mean: 3.5150939557708485 usec\nrounds: 45266"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 146310.65029709705,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010286082094838608",
            "extra": "mean: 6.834772437750836 usec\nrounds: 24345"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 63452.155448542115,
            "unit": "iter/sec",
            "range": "stddev: 0.00043934527866291685",
            "extra": "mean: 15.75990591542586 usec\nrounds: 22044"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8234385.5723038735,
            "unit": "iter/sec",
            "range": "stddev: 1.0580355279622409e-8",
            "extra": "mean: 121.44196931510291 nsec\nrounds: 80561"
          }
        ]
      }
    ]
  }
}