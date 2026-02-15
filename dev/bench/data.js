window.BENCHMARK_DATA = {
  "lastUpdate": 1771183204061,
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
          "id": "409a6768cf8c4075c25d0c008a5c21783fb8c314",
          "message": "Merge pull request #13 from nikolasil/add-create-release-workflow\n\nfix: resolve benchmark CI issues - permissions and summary size",
          "timestamp": "2026-02-14T17:41:19-05:00",
          "tree_id": "ba50a905654fc7f1ac847d3328722d06ef34b04c",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/409a6768cf8c4075c25d0c008a5c21783fb8c314"
        },
        "date": 1771109020499,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 205362.0845073412,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019433236856921686",
            "extra": "mean: 4.869448040513303 usec\nrounds: 15387"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 199792.90036397145,
            "unit": "iter/sec",
            "range": "stddev: 8.628921893569579e-7",
            "extra": "mean: 5.005182857740472 usec\nrounds: 37953"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 199457.81935250942,
            "unit": "iter/sec",
            "range": "stddev: 7.588183880757218e-7",
            "extra": "mean: 5.013591361051942 usec\nrounds: 22225"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 307808.08899384993,
            "unit": "iter/sec",
            "range": "stddev: 7.092553869127156e-7",
            "extra": "mean: 3.248777520008515 usec\nrounds: 46993"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 429351.3573702524,
            "unit": "iter/sec",
            "range": "stddev: 7.206584354511035e-7",
            "extra": "mean: 2.3290947678026024 usec\nrounds: 95887"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 444335.31979406724,
            "unit": "iter/sec",
            "range": "stddev: 5.919508959134003e-7",
            "extra": "mean: 2.2505525792175662 usec\nrounds: 88961"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5896288.28967601,
            "unit": "iter/sec",
            "range": "stddev: 2.480576914085623e-8",
            "extra": "mean: 169.59822024828694 nsec\nrounds: 197668"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51290.07430920149,
            "unit": "iter/sec",
            "range": "stddev: 0.000002427245356390301",
            "extra": "mean: 19.496949721139302 usec\nrounds: 12192"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 89801.00653812608,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014137028914283343",
            "extra": "mean: 11.135732644326634 usec\nrounds: 34254"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 21161.830840551873,
            "unit": "iter/sec",
            "range": "stddev: 0.0000053282094341712965",
            "extra": "mean: 47.25489054017603 usec\nrounds: 6998"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42486.351355288556,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027316670619846786",
            "extra": "mean: 23.536970535256927 usec\nrounds: 16664"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 8939.083080321707,
            "unit": "iter/sec",
            "range": "stddev: 0.000006221859231776179",
            "extra": "mean: 111.86829689516783 usec\nrounds: 4638"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4523.903568452108,
            "unit": "iter/sec",
            "range": "stddev: 0.0000633630977612194",
            "extra": "mean: 221.04803625205446 usec\nrounds: 1793"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20062.91229435159,
            "unit": "iter/sec",
            "range": "stddev: 0.00000547371818698063",
            "extra": "mean: 49.8432124573228 usec\nrounds: 9376"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1911245.1254295434,
            "unit": "iter/sec",
            "range": "stddev: 9.774422904748071e-8",
            "extra": "mean: 523.219123855319 nsec\nrounds: 178891"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 242871.69515740924,
            "unit": "iter/sec",
            "range": "stddev: 8.708289845958605e-7",
            "extra": "mean: 4.117400339104494 usec\nrounds: 27719"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1780456.6514909521,
            "unit": "iter/sec",
            "range": "stddev: 5.986226651134169e-8",
            "extra": "mean: 561.6536629310203 nsec\nrounds: 67719"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1296348.9989585334,
            "unit": "iter/sec",
            "range": "stddev: 1.2804161625415156e-7",
            "extra": "mean: 771.3972092416909 nsec\nrounds: 158153"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285653.4244624677,
            "unit": "iter/sec",
            "range": "stddev: 7.415584772994445e-7",
            "extra": "mean: 3.5007457091815506 usec\nrounds: 39561"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148316.0368968774,
            "unit": "iter/sec",
            "range": "stddev: 9.76533882593632e-7",
            "extra": "mean: 6.7423592277839095 usec\nrounds: 23879"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64619.09341346847,
            "unit": "iter/sec",
            "range": "stddev: 0.0004206903400349637",
            "extra": "mean: 15.475302223778511 usec\nrounds: 23294"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8033020.602997869,
            "unit": "iter/sec",
            "range": "stddev: 1.1179051547207441e-8",
            "extra": "mean: 124.48617393404739 nsec\nrounds: 78846"
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
          "id": "3baac68beccd66a7867ba0300e88961d2188cbca",
          "message": "Merge pull request #14 from nikolasil/add-create-release-workflow\n\nfix: add -u flag to git-cliff for unreleased changelog",
          "timestamp": "2026-02-14T17:47:31-05:00",
          "tree_id": "e415ca443adcd028720ece55d6a3d6b541a8a52d",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/3baac68beccd66a7867ba0300e88961d2188cbca"
        },
        "date": 1771109401715,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 203408.0796334615,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017262201901549167",
            "extra": "mean: 4.916225558994442 usec\nrounds: 16683"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 203542.28943985893,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017462260552939167",
            "extra": "mean: 4.912983944279905 usec\nrounds: 37370"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 201149.4249694333,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018760302717217328",
            "extra": "mean: 4.971428579286071 usec\nrounds: 36348"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 305879.75728789216,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010352629246409738",
            "extra": "mean: 3.269258511470591 usec\nrounds: 44323"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 440804.68253454496,
            "unit": "iter/sec",
            "range": "stddev: 5.620824523797461e-7",
            "extra": "mean: 2.2685784421576147 usec\nrounds: 97097"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 445139.495621558,
            "unit": "iter/sec",
            "range": "stddev: 5.207945019973799e-7",
            "extra": "mean: 2.2464867975906704 usec\nrounds: 93809"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5803608.470246814,
            "unit": "iter/sec",
            "range": "stddev: 2.32248312092322e-8",
            "extra": "mean: 172.306592549558 nsec\nrounds: 191571"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 50828.44191859647,
            "unit": "iter/sec",
            "range": "stddev: 0.000002121789362182132",
            "extra": "mean: 19.67402427171651 usec\nrounds: 13184"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 88676.84207460815,
            "unit": "iter/sec",
            "range": "stddev: 0.000001340983925426292",
            "extra": "mean: 11.276901348817216 usec\nrounds: 38702"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20041.09799400459,
            "unit": "iter/sec",
            "range": "stddev: 0.00000863691854116887",
            "extra": "mean: 49.89746571266483 usec\nrounds: 7408"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42475.491600550384,
            "unit": "iter/sec",
            "range": "stddev: 0.000002837277146623971",
            "extra": "mean: 23.542988257893228 usec\nrounds: 16692"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9117.118451045286,
            "unit": "iter/sec",
            "range": "stddev: 0.0000073758847843022474",
            "extra": "mean: 109.68377841853629 usec\nrounds: 4161"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4429.050977097437,
            "unit": "iter/sec",
            "range": "stddev: 0.00006438162632966876",
            "extra": "mean: 225.782002774632 usec\nrounds: 1802"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19665.483551043108,
            "unit": "iter/sec",
            "range": "stddev: 0.000006440033227545329",
            "extra": "mean: 50.85051671393849 usec\nrounds: 9483"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1937023.6136432996,
            "unit": "iter/sec",
            "range": "stddev: 1.0446883217138329e-7",
            "extra": "mean: 516.2559676384736 nsec\nrounds: 177936"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 243321.59898731302,
            "unit": "iter/sec",
            "range": "stddev: 8.314165081215542e-7",
            "extra": "mean: 4.1097872287619674 usec\nrounds: 36034"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1782407.7208255033,
            "unit": "iter/sec",
            "range": "stddev: 6.209885917642776e-8",
            "extra": "mean: 561.0388623860118 nsec\nrounds: 69171"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1296322.4115729423,
            "unit": "iter/sec",
            "range": "stddev: 1.2313956087473613e-7",
            "extra": "mean: 771.4130304872278 nsec\nrounds: 159439"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285465.9012368432,
            "unit": "iter/sec",
            "range": "stddev: 6.878285241283235e-7",
            "extra": "mean: 3.503045357316871 usec\nrounds: 52340"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 146523.92159431972,
            "unit": "iter/sec",
            "range": "stddev: 9.444376244882574e-7",
            "extra": "mean: 6.824824159216108 usec\nrounds: 28486"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 61556.668938089104,
            "unit": "iter/sec",
            "range": "stddev: 0.0004274572460545556",
            "extra": "mean: 16.245193530627112 usec\nrounds: 18178"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8107964.77657223,
            "unit": "iter/sec",
            "range": "stddev: 1.0624365973211877e-8",
            "extra": "mean: 123.33551360389123 nsec\nrounds: 80490"
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
          "id": "e9a34cfc57e0bd3a5dd88ea00552ff50d25b4b4e",
          "message": "Merge pull request #15 from nikolasil/add-create-release-workflow\n\nfix: remove conflicting OUTPUT env from git-cliff action",
          "timestamp": "2026-02-14T17:50:49-05:00",
          "tree_id": "ed0ac0ba34f6fca055316a5ffeec09f966f4c359",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/e9a34cfc57e0bd3a5dd88ea00552ff50d25b4b4e"
        },
        "date": 1771109598432,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 208528.27298638807,
            "unit": "iter/sec",
            "range": "stddev: 0.000001787346377211716",
            "extra": "mean: 4.79551278912321 usec\nrounds: 15521"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 209099.04187807778,
            "unit": "iter/sec",
            "range": "stddev: 7.706914089602418e-7",
            "extra": "mean: 4.782422678833141 usec\nrounds: 38450"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 203450.45938345033,
            "unit": "iter/sec",
            "range": "stddev: 6.964351115507064e-7",
            "extra": "mean: 4.915201484579911 usec\nrounds: 36509"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 306044.0704860228,
            "unit": "iter/sec",
            "range": "stddev: 7.504951945598198e-7",
            "extra": "mean: 3.2675032664802783 usec\nrounds: 43778"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 433952.18143407936,
            "unit": "iter/sec",
            "range": "stddev: 4.928693710856227e-7",
            "extra": "mean: 2.3044013667480723 usec\nrounds: 41852"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 439237.20982783375,
            "unit": "iter/sec",
            "range": "stddev: 5.361086217413561e-7",
            "extra": "mean: 2.27667414696484 usec\nrounds: 97857"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5670318.081316582,
            "unit": "iter/sec",
            "range": "stddev: 2.1879280076523074e-8",
            "extra": "mean: 176.3569495853478 nsec\nrounds: 197239"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51458.299214892904,
            "unit": "iter/sec",
            "range": "stddev: 0.000002169957554326658",
            "extra": "mean: 19.433211265377054 usec\nrounds: 12605"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 86270.1158141504,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013304208891563058",
            "extra": "mean: 11.591499449870632 usec\nrounds: 39081"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 21042.054647012363,
            "unit": "iter/sec",
            "range": "stddev: 0.000005203421215640608",
            "extra": "mean: 47.52387619818221 usec\nrounds: 7407"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42990.3051653305,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028930897849841025",
            "extra": "mean: 23.261058421293768 usec\nrounds: 16672"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9116.077588478012,
            "unit": "iter/sec",
            "range": "stddev: 0.000005553405707971126",
            "extra": "mean: 109.69630197793833 usec\nrounds: 4348"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4476.774785869503,
            "unit": "iter/sec",
            "range": "stddev: 0.00005621957259855532",
            "extra": "mean: 223.3750965441463 usec\nrounds: 1823"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19879.507281720256,
            "unit": "iter/sec",
            "range": "stddev: 0.000005723391590114814",
            "extra": "mean: 50.303057607445176 usec\nrounds: 9287"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1872453.411784999,
            "unit": "iter/sec",
            "range": "stddev: 7.73961645457176e-8",
            "extra": "mean: 534.0586813568102 nsec\nrounds: 181160"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 245964.92103837573,
            "unit": "iter/sec",
            "range": "stddev: 6.689949080360651e-7",
            "extra": "mean: 4.065620397324783 usec\nrounds: 33975"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1767339.755804413,
            "unit": "iter/sec",
            "range": "stddev: 5.344316866884398e-8",
            "extra": "mean: 565.8221610845975 nsec\nrounds: 69604"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1283862.8895685463,
            "unit": "iter/sec",
            "range": "stddev: 1.1480335842344425e-7",
            "extra": "mean: 778.8993732314013 nsec\nrounds: 157208"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 287795.3654385482,
            "unit": "iter/sec",
            "range": "stddev: 6.554021373580427e-7",
            "extra": "mean: 3.4746911176841935 usec\nrounds: 53263"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 146941.18472539005,
            "unit": "iter/sec",
            "range": "stddev: 9.430000792733426e-7",
            "extra": "mean: 6.805443973170916 usec\nrounds: 17447"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 65021.19507943279,
            "unit": "iter/sec",
            "range": "stddev: 0.0003890968670892543",
            "extra": "mean: 15.379600433033497 usec\nrounds: 23553"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8060605.814442196,
            "unit": "iter/sec",
            "range": "stddev: 1.0656761987866767e-8",
            "extra": "mean: 124.06015416473339 nsec\nrounds: 80109"
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
          "id": "83906c0717d09a5a60e4a2eb1e0ff8983d9d7fa1",
          "message": "Merge pull request #16 from nikolasil/add-create-release-workflow\n\nAdd create release workflow",
          "timestamp": "2026-02-14T18:14:52-05:00",
          "tree_id": "26b68aec8c7051f7d86d83354ac33915bea68313",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/83906c0717d09a5a60e4a2eb1e0ff8983d9d7fa1"
        },
        "date": 1771111057795,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 207330.571012988,
            "unit": "iter/sec",
            "range": "stddev: 0.000001629079327257537",
            "extra": "mean: 4.823215385527281 usec\nrounds: 16756"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 206169.5988738288,
            "unit": "iter/sec",
            "range": "stddev: 7.799387899403793e-7",
            "extra": "mean: 4.850375639581943 usec\nrounds: 37134"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 204037.61647688737,
            "unit": "iter/sec",
            "range": "stddev: 7.213987721334858e-7",
            "extra": "mean: 4.901057056375074 usec\nrounds: 36350"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 307385.15280343307,
            "unit": "iter/sec",
            "range": "stddev: 6.477380283718603e-7",
            "extra": "mean: 3.253247565406911 usec\nrounds: 41383"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 436283.6942086843,
            "unit": "iter/sec",
            "range": "stddev: 5.778368017591622e-7",
            "extra": "mean: 2.2920865786968365 usec\nrounds: 99424"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 449161.53889163287,
            "unit": "iter/sec",
            "range": "stddev: 5.039932745523242e-7",
            "extra": "mean: 2.2263705001715772 usec\nrounds: 100726"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5667810.905806347,
            "unit": "iter/sec",
            "range": "stddev: 2.1907228900039464e-8",
            "extra": "mean: 176.4349616842714 nsec\nrounds: 196503"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51170.85378507489,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018188170889435011",
            "extra": "mean: 19.542374731524845 usec\nrounds: 13503"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 88430.11618104897,
            "unit": "iter/sec",
            "range": "stddev: 0.000001337682484796155",
            "extra": "mean: 11.30836465206754 usec\nrounds: 38039"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20650.95485971584,
            "unit": "iter/sec",
            "range": "stddev: 0.0000050018418530077734",
            "extra": "mean: 48.42391099070759 usec\nrounds: 6460"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43048.505882359364,
            "unit": "iter/sec",
            "range": "stddev: 0.000002681096449263409",
            "extra": "mean: 23.229609936585167 usec\nrounds: 17028"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9122.272062402493,
            "unit": "iter/sec",
            "range": "stddev: 0.000005119047160298192",
            "extra": "mean: 109.62181276323767 usec\nrounds: 4748"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4572.556431293821,
            "unit": "iter/sec",
            "range": "stddev: 0.00008171799478438444",
            "extra": "mean: 218.69604345529015 usec\nrounds: 1887"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19925.129966645083,
            "unit": "iter/sec",
            "range": "stddev: 0.0000051418290933210255",
            "extra": "mean: 50.187878406515416 usec\nrounds: 9614"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1902152.9854296376,
            "unit": "iter/sec",
            "range": "stddev: 7.128968434922987e-8",
            "extra": "mean: 525.7200696578728 nsec\nrounds: 165810"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244610.84693145027,
            "unit": "iter/sec",
            "range": "stddev: 6.83207942322872e-7",
            "extra": "mean: 4.088126150351132 usec\nrounds: 35751"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1760525.3654830311,
            "unit": "iter/sec",
            "range": "stddev: 5.3048579697090125e-8",
            "extra": "mean: 568.012264751356 nsec\nrounds: 69076"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1288313.6030201537,
            "unit": "iter/sec",
            "range": "stddev: 1.2493132266147712e-7",
            "extra": "mean: 776.2085238063752 nsec\nrounds: 159694"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286803.9505669032,
            "unit": "iter/sec",
            "range": "stddev: 6.33232583939544e-7",
            "extra": "mean: 3.4867023206039427 usec\nrounds: 52701"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 149609.11112705618,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010638300486103408",
            "extra": "mean: 6.684084896077925 usec\nrounds: 30449"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 65363.42438619958,
            "unit": "iter/sec",
            "range": "stddev: 0.0003867421875957556",
            "extra": "mean: 15.299076041235283 usec\nrounds: 24513"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8030671.844448482,
            "unit": "iter/sec",
            "range": "stddev: 1.011019453184154e-8",
            "extra": "mean: 124.52258283872972 nsec\nrounds: 79854"
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
          "id": "38adc60ecea124b4e316f406a480d4d613bae342",
          "message": "Merge pull request #17 from nikolasil/add-create-release-workflow\n\nfix: add checkout step to create-tag job",
          "timestamp": "2026-02-15T13:54:25-05:00",
          "tree_id": "c49e81c1ba4aaf5c32005362933f3fe8edf8548f",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/38adc60ecea124b4e316f406a480d4d613bae342"
        },
        "date": 1771181814390,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 207550.8123383504,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016944569063453106",
            "extra": "mean: 4.818097258852424 usec\nrounds: 16708"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 208481.01814945097,
            "unit": "iter/sec",
            "range": "stddev: 7.922537567217035e-7",
            "extra": "mean: 4.796599752228491 usec\nrounds: 37132"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 189240.04091698487,
            "unit": "iter/sec",
            "range": "stddev: 0.000001818293481739528",
            "extra": "mean: 5.284293932480581 usec\nrounds: 37808"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 304655.21434910235,
            "unit": "iter/sec",
            "range": "stddev: 6.588057581796682e-7",
            "extra": "mean: 3.28239909543812 usec\nrounds: 43115"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 431859.3753406785,
            "unit": "iter/sec",
            "range": "stddev: 6.311959006354689e-7",
            "extra": "mean: 2.315568578802152 usec\nrounds: 96349"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 451433.74252458813,
            "unit": "iter/sec",
            "range": "stddev: 5.353556046227369e-7",
            "extra": "mean: 2.215164498798034 usec\nrounds: 102481"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5788890.448376119,
            "unit": "iter/sec",
            "range": "stddev: 2.2740088609152064e-8",
            "extra": "mean: 172.74467515284806 nsec\nrounds: 195351"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51903.349411595045,
            "unit": "iter/sec",
            "range": "stddev: 0.000001992531865789146",
            "extra": "mean: 19.26657935059203 usec\nrounds: 13705"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 89357.3911252374,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014164800450852272",
            "extra": "mean: 11.191016069375463 usec\nrounds: 37836"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 21003.790768331073,
            "unit": "iter/sec",
            "range": "stddev: 0.000005679622811415642",
            "extra": "mean: 47.610453323871994 usec\nrounds: 7145"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43818.756792065695,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029186520156320155",
            "extra": "mean: 22.82127730700637 usec\nrounds: 17230"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9148.116009330863,
            "unit": "iter/sec",
            "range": "stddev: 0.00000580182830279908",
            "extra": "mean: 109.31212492058731 usec\nrounds: 4715"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4433.219568403475,
            "unit": "iter/sec",
            "range": "stddev: 0.00006931590206135371",
            "extra": "mean: 225.56969817764465 usec\nrounds: 1756"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20048.625359670696,
            "unit": "iter/sec",
            "range": "stddev: 0.000005683894878544157",
            "extra": "mean: 49.87873143719741 usec\nrounds: 9212"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1882809.9104479977,
            "unit": "iter/sec",
            "range": "stddev: 1.1447893324697614e-7",
            "extra": "mean: 531.1210624348472 nsec\nrounds: 166918"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244400.78121876897,
            "unit": "iter/sec",
            "range": "stddev: 7.872024027006686e-7",
            "extra": "mean: 4.091639948993764 usec\nrounds: 35295"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1768772.5006509735,
            "unit": "iter/sec",
            "range": "stddev: 6.104739323809657e-8",
            "extra": "mean: 565.3638326194358 nsec\nrounds: 69459"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1292761.1140022224,
            "unit": "iter/sec",
            "range": "stddev: 1.3171876786816895e-7",
            "extra": "mean: 773.5381186580872 nsec\nrounds: 180148"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285524.5803025271,
            "unit": "iter/sec",
            "range": "stddev: 6.869904240198872e-7",
            "extra": "mean: 3.5023254353108637 usec\nrounds: 53009"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148945.4276508274,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010422373239017266",
            "extra": "mean: 6.713868399802772 usec\nrounds: 28389"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64338.20865254859,
            "unit": "iter/sec",
            "range": "stddev: 0.0004295810759936361",
            "extra": "mean: 15.542863578940937 usec\nrounds: 24549"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8129997.939265755,
            "unit": "iter/sec",
            "range": "stddev: 1.1010987655358637e-8",
            "extra": "mean: 123.00126118989931 nsec\nrounds: 77078"
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
          "id": "bdec3542dc3be0eca7c96d1dd5382dedb09fd247",
          "message": "Merge pull request #18 from nikolasil/add-create-release-workflow\n\nfix: use release files from prepare for building, only commit if chan…",
          "timestamp": "2026-02-15T14:17:32-05:00",
          "tree_id": "02399e607158f4023c19b085447af1972409040a",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/bdec3542dc3be0eca7c96d1dd5382dedb09fd247"
        },
        "date": 1771183203230,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 206401.73961688284,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016267513041212174",
            "extra": "mean: 4.844920405497416 usec\nrounds: 17363"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 201607.20949982488,
            "unit": "iter/sec",
            "range": "stddev: 0.000001193045416302562",
            "extra": "mean: 4.960140078725054 usec\nrounds: 38614"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 203621.60832020146,
            "unit": "iter/sec",
            "range": "stddev: 7.28371838248255e-7",
            "extra": "mean: 4.9110701376421115 usec\nrounds: 38567"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 309758.00159627583,
            "unit": "iter/sec",
            "range": "stddev: 6.241820088898427e-7",
            "extra": "mean: 3.2283266125384986 usec\nrounds: 44340"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 431875.5355149708,
            "unit": "iter/sec",
            "range": "stddev: 5.186976049082276e-7",
            "extra": "mean: 2.3154819334871437 usec\nrounds: 106191"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 439940.853038138,
            "unit": "iter/sec",
            "range": "stddev: 6.479633376784003e-7",
            "extra": "mean: 2.273032824967749 usec\nrounds: 108850"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5733330.514900015,
            "unit": "iter/sec",
            "range": "stddev: 2.3880585873637866e-8",
            "extra": "mean: 174.41869039316308 nsec\nrounds: 198020"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52226.08826654825,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017891907380350666",
            "extra": "mean: 19.14751866722743 usec\nrounds: 10955"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 87522.65902649522,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015283689100013874",
            "extra": "mean: 11.42561264846028 usec\nrounds: 40005"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20846.487555179134,
            "unit": "iter/sec",
            "range": "stddev: 0.000005858849089287324",
            "extra": "mean: 47.96971179691893 usec\nrounds: 7519"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42648.98918852831,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025977931811164353",
            "extra": "mean: 23.447214553656508 usec\nrounds: 17329"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9121.822466620875,
            "unit": "iter/sec",
            "range": "stddev: 0.000004705256969197409",
            "extra": "mean: 109.62721579588514 usec\nrounds: 4824"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4071.555111793739,
            "unit": "iter/sec",
            "range": "stddev: 0.00007782811018664732",
            "extra": "mean: 245.6064016187285 usec\nrounds: 1977"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19999.965064861855,
            "unit": "iter/sec",
            "range": "stddev: 0.000005027187564400521",
            "extra": "mean: 50.000087337997925 usec\nrounds: 9572"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1892373.9262112686,
            "unit": "iter/sec",
            "range": "stddev: 7.730462074865371e-8",
            "extra": "mean: 528.4367883899746 nsec\nrounds: 181819"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 243444.13531141434,
            "unit": "iter/sec",
            "range": "stddev: 7.346428596176294e-7",
            "extra": "mean: 4.107718588992902 usec\nrounds: 36683"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1730322.6922954987,
            "unit": "iter/sec",
            "range": "stddev: 6.162606189783092e-8",
            "extra": "mean: 577.9268829176427 nsec\nrounds: 67714"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1277736.689925303,
            "unit": "iter/sec",
            "range": "stddev: 1.2551219529877484e-7",
            "extra": "mean: 782.6338618002045 nsec\nrounds: 181786"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286497.57940331835,
            "unit": "iter/sec",
            "range": "stddev: 6.364290758703275e-7",
            "extra": "mean: 3.4904308863016436 usec\nrounds: 53752"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147141.7154140971,
            "unit": "iter/sec",
            "range": "stddev: 9.688014409511808e-7",
            "extra": "mean: 6.796169238517615 usec\nrounds: 29875"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 65753.26865256767,
            "unit": "iter/sec",
            "range": "stddev: 0.00037186540835013634",
            "extra": "mean: 15.208369416338513 usec\nrounds: 23954"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8141804.73269818,
            "unit": "iter/sec",
            "range": "stddev: 1.0212498718917436e-8",
            "extra": "mean: 122.82289158626159 nsec\nrounds: 80174"
          }
        ]
      }
    ]
  }
}