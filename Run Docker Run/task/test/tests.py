from pathlib import Path

import docker
from hstest import StageTest, dynamic_test, CheckResult

stage = Path(__file__).parent.parent

project_images = ["python:3.11-slim", "hyper-web-app"]


class DockerTest(StageTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = None
        self.client = docker.from_env()

    @dynamic_test()
    def test1(self):
        print('DockerRootDir ' + self.client.info().get('DockerRootDir'))
        images_docker = self.client.images.list(all=True)
        for image in images_docker:
            print('images in the docker ' + str(image.tags))
        """Tests if image exists in the system"""
        images_text = " ".join([str(image) for image in self.client.images.list()])
        print('images_text ' + images_text)
        for image in project_images:
            if image not in images_text:
                return CheckResult.wrong(f"'{image}' not found in the system images!")

        return CheckResult.correct()


if __name__ == '__main__':
    DockerTest().run_tests()
