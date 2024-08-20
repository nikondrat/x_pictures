import 'package:flutter/foundation.dart';
import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'jobs.g.dart';

class JobsStore extends _JobsStore with _$JobsStore {
  JobsStore({required super.restClient});
}

abstract class _JobsStore with Store {
  final RestClient restClient;

  _JobsStore({required this.restClient});

  JobsBody body = JobsBody(
    count: 0,
    total: 0,
    nextUrl: '',
    previousUrl: '',
    jobs: [],
  );

  @observable
  ObservableFuture<List<JobModel>> fetchJobsFuture = emptyResponse;

  @observable
  ObservableList<JobModel> jobs = ObservableList();

  @action
  Future<List<JobModel>> fetchJobs() async {
    final future = restClient.get(Endpoint().jobs).then((v) {
      body = JobsBody.fromJson(v!);

      // TODO only for dev

      return JobsBody(
        count: 0,
        total: 0,
        nextUrl: null,
        previousUrl: null,
        jobs: [
          JobModel(
              id: 0,
              status: Status.completed,
              createdDate: DateTime.now(),
              estimatedTime: 0,
              estimatedTimestamp: 0,
              images: [
                MediaModel(
                    type: MediaType.image,
                    url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg',
                    createdDate: DateTime.now()),
                MediaModel(
                    type: MediaType.image,
                    url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg',
                    createdDate: DateTime.now()),
                MediaModel(
                    type: MediaType.image,
                    url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg',
                    createdDate: DateTime.now()),
                MediaModel(
                    type: MediaType.image,
                    url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg',
                    createdDate: DateTime.now()),
                // ImageModel(
                //     id: 0,
                //     url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
                // ImageModel(
                //     id: 0,
                //     url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
                // ImageModel(
                //     id: 0,
                //     url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
                // ImageModel(
                //     id: 0,
                //     url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
              ],
              cost: '',
              timeSpent: 0,
              pack: PackModel(
                  id: 0,
                  title: 'dfgfgd',
                  description: 'sdfsdfs',
                  category: 'Pinterest',
                  images: [
                    MediaModel(
                        id: 0,
                        url:
                            'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
                    MediaModel(
                        id: 0,
                        url:
                            'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
                    MediaModel(
                        id: 0,
                        url:
                            'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
                    MediaModel(
                        id: 0,
                        url:
                            'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
                  ]),
              lora: LoraModel(
                  id: '',
                  status: Status.completed,
                  estimatedTime: 0,
                  estimatedTimestamp: 0,
                  trainingTimeSeconds: 0,
                  images: [],
                  cost: '',
                  createdDate: DateTime.now()))
        ],
      ).jobs;
      return body.jobs;
    }).catchError((v) {
      // TODO only for dev
      return JobsBody(
        count: 0,
        total: 0,
        nextUrl: '',
        previousUrl: '',
        jobs: [
          JobModel(
              id: 0,
              status: Status.completed,
              createdDate: DateTime.now(),
              estimatedTime: 0,
              estimatedTimestamp: 0,
              images: [
                MediaModel(
                    type: MediaType.image,
                    url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg',
                    createdDate: DateTime.now()),
                MediaModel(
                    type: MediaType.image,
                    url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg',
                    createdDate: DateTime.now()),
                MediaModel(
                    type: MediaType.image,
                    url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg',
                    createdDate: DateTime.now()),
                MediaModel(
                    type: MediaType.image,
                    url: 'https://telegra.ph/file/299a9e951b4472a5832ef.jpg',
                    createdDate: DateTime.now()),
              ],
              cost: '',
              timeSpent: 0,
              pack: PackModel(
                  id: 0,
                  title: 'dfgfgd',
                  description: 'sdfsdfs',
                  category: 'Pinterest',
                  images: [
                    MediaModel(
                        id: 0,
                        url:
                            'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
                    MediaModel(
                        id: 0,
                        url:
                            'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
                    MediaModel(
                        id: 0,
                        url:
                            'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
                    MediaModel(
                        id: 0,
                        url:
                            'https://telegra.ph/file/299a9e951b4472a5832ef.jpg'),
                  ]),
              lora: LoraModel(
                  id: '',
                  status: Status.completed,
                  estimatedTime: 0,
                  estimatedTimestamp: 0,
                  trainingTimeSeconds: 0,
                  images: [],
                  cost: '',
                  createdDate: DateTime.now()))
        ],
      ).jobs;
    });
    fetchJobsFuture = ObservableFuture(future);

    return jobs = ObservableList.of(await future);
  }

  @computed
  bool get hasResults =>
      fetchJobsFuture != emptyResponse &&
      fetchJobsFuture.status == FutureStatus.fulfilled;

  static ObservableFuture<List<JobModel>> emptyResponse =
      ObservableFuture.value([]);

  void createJob() {
    restClient.post(Endpoint().jobs, body: {}).then((v) {
      final JobModel job = JobModel.fromJson(v!);
    });
  }

  Future<JobModel?> getJob(String id) async {
    final future = restClient.get('${Endpoint().jobs}/$id').then((v) {
      final JobModel job = JobModel.fromJson(v!);
      return job;
    });
    return await future;
  }
}
